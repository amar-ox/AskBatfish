# tools.py

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# 2024 Amar Abane

# Description: This file is part of the AskBatfish project which interacts with
# Batfish using LLMs.


from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Neo4jVector
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

import json
import os
from dotenv import load_dotenv


load_dotenv(".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
neo4j_url = os.getenv("NEO4J_URI")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")



def remove_python_code_fence(input_string):
    if input_string.startswith("```"):
        input_string = input_string[3:]
    if input_string.endswith("```"):
        input_string = input_string[:-3]
    if input_string.startswith("python"):
        input_string = input_string[6:]
    return input_string.strip('\n')


def create_ask_chain(model):
    graph = Neo4jGraph (
        url=neo4j_url, 
        username=neo4j_username, 
        password=neo4j_password
    )

    llm = ChatOpenAI(model_name=model, temperature=0)
    
    examples = []
    try:
        with open("bf_questions.json", 'r') as file:
            text = file.read()
            examples = json.loads(text)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        
    example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples,
            OpenAIEmbeddings(),
            Neo4jVector,
            k=3,
            input_keys=["question"],
    )
    
    example_prompt = PromptTemplate.from_template("Question: {question}\nInvocation: {invocation}")

    prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix="""You are the co-pilote of a network engineer. 
Pick up the simplest case from the examples below and check if the input query contains the minimal information to generate the pybatfish invocation. 
First try to infer implicit information or find default values.
Then, if the query has the minimal information, answer with 'OK'. Otherwise, answer by giving:
    - the missing minimal information.
    - an example of correct formulation for the query with minimal information.

Examples:""",
        suffix="Input query: {question}.\n\nDo not include pybatfish invocations in your answer.",
        input_variables=["question"],
    )
    
    output_parser = StrOutputParser()

    ask_chain = (
        prompt | llm | output_parser
    )

    return ask_chain


def create_text_to_code_chain(model):
    graph = Neo4jGraph (
        url=neo4j_url, 
        username=neo4j_username, 
        password=neo4j_password
    )
    graph.refresh_schema()

    llm = ChatOpenAI(model_name=model, temperature=0)
    
    examples = []
    try:
        with open("bf_questions.json", 'r') as file:
            text = file.read()
            examples = json.loads(text)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        
    example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples,
            OpenAIEmbeddings(),
            Neo4jVector,
            k=3,
            input_keys=["question"],
    )
    
    example_prompt = PromptTemplate.from_template("Question: {question}\nInvocation: {invocation}")
    prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        prefix="""You are the co-pilote of a network engineer. Given the input task, complete the Python function template with the correct pybatfish invocation and return a dataframe.
        
Function template:
```
def run():
    try:
        # call bf.q. and get answer object
        if hasattr(answer, 'frame') and callable(getattr(answer, 'frame')):
            return answer.frame()
        else:
            return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()
``` 

Rely on the examples below to generate the correct pybatfish invocation:""",
        example_prompt=example_prompt,
        suffix="""\nInput task: {question}

Answer only with the completed function, --no initialization, no explanation, and no code fences.""",
        input_variables=["question"],
    )
    
    output_parser = StrOutputParser()

    text_to_code_chain = (
        prompt | llm | output_parser
    )

    # print(prompt.format(task="get routing tables of as1border1"))
    return text_to_code_chain


def create_data_to_text_chain(model):
    template = """You are a network engineer. You received a query from a network operator regarding the network status.
They executed a verification query and provided the results in Markdown table format.
Analyze the table and explain the problem to the operator.

Markdown Table:

```
{data}
```

Short and concise analysis:
"""

    llm = ChatOpenAI(model_name=model, temperature=0)
    prompt = ChatPromptTemplate.from_template(template)
    output_parser = StrOutputParser()
    data_to_text_chain = (
        {"data": RunnablePassthrough()} 
        | prompt | llm | output_parser
    )
    return data_to_text_chain



def create_generate_tasks_chain():
    template = """You are a network engineer doing a demonstration of a Batfish network verification software. Rely on the network information below and the example questions to generate 5 network verification tasks with actual values.
Answer only with the 5 tasks, --no explanation, no expected result, and no additional text. 

Nodes:
{devices}

Interfaces:
{interfaces}

Example questions:
1- Show the routing table of node x.
2- Retrieve routes in the BGP RIB.
3- Examine the longest prefix match routes for IP=X  on node Y.
4- Retrieve all Layer 3 links in the network.
5- List the properties of BGP peers for node X.
6- Retrieve configuration parameters for all OSPF areas.
7- List defined structures of type 'bgp neighbor' on node A.
8- Identify nodes with defined but unused structures.
9- How is the flow with source IP=X and destination IP=Y for DNS traffic processed by the router A?
10- Find filter lines matching DNS traffic.
11- Trace the paths for a flow from source IP=X to destination IP=Y starting at interface I?
12- What is the compatibility of configured BGP sessions?
"""

    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    prompt = ChatPromptTemplate.from_template(template)
    output_parser = StrOutputParser()
    data_to_text_chain = (
        {
            "devices": RunnablePassthrough(), "interfaces": RunnablePassthrough()
        }
        | prompt | llm | output_parser
    )
    return data_to_text_chain



def create_parsing_status_chain():
    template = """You are a network engineer. You executed a parsing of configuration files and got the results in Markdown table format.
Analyze the tables and explain the current status to the operator in a short and concise reponse.

Markdown Tables:


{data}
"""

    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    prompt = ChatPromptTemplate.from_template(template)
    output_parser = StrOutputParser()
    parsing_status_chain = (
        {"data": RunnablePassthrough()} 
        | prompt | llm | output_parser
    )
    return parsing_status_chain