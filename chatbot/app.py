# app.py

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
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import tool
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor

from typing import List, Optional
import chainlit as cl

from tools import (
    remove_python_code_fence, 
    create_text_to_code_chain, 
    create_data_to_text_chain,
    create_ask_chain, 
    create_generate_tasks_chain, 
    create_parsing_status_chain
)
from langchain.tools import BaseTool

import os
from dotenv import load_dotenv
import re
from io import StringIO


## pybatfish imports
# Importing required libraries, setting up logging, and loading questions
import logging
import random  # noqa: F401
import pandas as pd

from pybatfish.client.session import Session  # noqa: F401

# noinspection PyUnresolvedReferences
from pybatfish.datamodel import Edge, Interface  # noqa: F401
from pybatfish.datamodel.answer import TableAnswer
from pybatfish.datamodel.flow import HeaderConstraints, PathConstraints  # noqa: F401
from pybatfish.datamodel.route import BgpRoute  # noqa: F401

from pandasai import SmartDataframe
from pandasai.llm import OpenAI

# Configure all pybatfish loggers to use WARN level
logging.getLogger("pybatfish").setLevel(logging.WARN)

load_dotenv(".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bf = None

ask_chain = None
text_to_code_chain = None
data_to_text_chain = None

def init_chains():
    global ask_chain,text_to_code_chain, data_to_text_chain
    profile = cl.user_session.get("chat_profile")
    model = "gpt-3.5-turbo" if profile == "Fast" else "gpt-4o"
    ask_chain = create_ask_chain(model)
    text_to_code_chain = create_text_to_code_chain(model)
    # data_to_text_chain = create_data_to_text_chain(model)

_basic_suffix = """### You are using the 'Basic' profile 🤖
 
You can now ask questions.

To help you create a query, you can use `/ask` before your query to check if it has enough information to run."""

_agent_suffix = """### You are using the '{profile}' profile 🤖 

You can now ask questions."""

def init_batfish(snapshot_path):
    global bf
    bf = Session(host="batfish")

    # Assign a friendly name to your network and snapshot
    NETWORK_NAME = "example_network"
    SNAPSHOT_NAME = "example_snapshot"

    SNAPSHOT_PATH = snapshot_path

    # Now create the network and initialize the snapshot
    bf.set_network(NETWORK_NAME)
    bf.init_snapshot(SNAPSHOT_PATH, name=SNAPSHOT_NAME, overwrite=True)
    bf.q.routes().answer()


@tool
def process_query(task: str) -> str:
    """Useful to answer text queries about the network's configuration or forwarding analysis."""
    
    local_namespace = {}
    
    output = text_to_code_chain.invoke(task)
    code = remove_python_code_fence(output)
    print(f"Generate invocation: {code}")
    
    globals_dict = globals().copy()
    globals_dict['bf'] = bf
    exec(code, globals_dict, local_namespace)
    run = local_namespace['run']
    try:
        result = run()
        if not result.empty:
            return result.to_markdown(index=False)
        else:
            return 'Got an empty result.'
    except Exception as e:
        print(f"Exception: {e}")
        return 'Unable to get a result.'

@tool
def explain_result(df: str) -> str:
    """Useful to explain the Markdown table resulting from a query."""
    response = data_to_text_chain.invoke({"data": df})
    return response

@tool
def analyze_df(md_df: str, question: str) -> str:
    """Useful to filter and manipulate a Markdown table using text queries."""
    
    profile = cl.user_session.get("chat_profile")
    model = "gpt-3.5-turbo" if profile == "Fast" else "gpt-4o"
    llm = OpenAI(model=model, temperature=0)

    # Convert Markdown table to DataFrame
    df = pd.read_csv(StringIO(md_df), delimiter='|', skiprows=1, skipinitialspace=True)
    df = df.iloc[:, 1:-1]
    df.columns = [col.strip() for col in df.columns]
    
    sdf = SmartDataframe(df, config={"llm": llm})
    response = sdf.chat(question)
    if isinstance(response, pd.core.frame.DataFrame):
        return response.to_markdown(index=False)
    return response



def generate_example_tasks():
    global bf

    chain = create_generate_tasks_chain()

    df = bf.q.nodeProperties().answer().frame()
    devices = df.head(5)[['Node','Interfaces']]

    df = bf.q.interfaceProperties().answer().frame()
    interfaces = df.head(5)[['Interface', 'Primary_Address']]
    
    response = chain.invoke({
        "devices": devices.to_markdown(), "interfaces": interfaces.to_markdown()
    })
    return response

def generate_parsing_status():
    global bf

    chain = create_parsing_status_chain()

    a = bf.q.fileParseStatus().answer().frame()
    b = bf.q.initIssues().answer().frame()

    data = f"File parse status:\n {a.to_markdown()}\n\nInit issues:\n {b.to_markdown()}"
    
    response = chain.invoke({"data": data})
    return response


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    if (username, password) == ("admin", "admin"):
        return cl.User(identifier="admin", metadata={"role": "admin", "provider": "credentials"})
    else:
        return None


def init_agent():
    profile = cl.user_session.get("chat_profile")
    model = "gpt-3.5-turbo" if profile == "Fast" else "gpt-4o"
    llm = ChatOpenAI(model_name=model, temperature=0, streaming=True)

    MEMORY_KEY = "chat_history"
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are the co-pilot of a network engineer.
                Answer the query you are asked using the provided tools.
                You can ask the human for more clarifications if the task is ambiguous or if you are not sure about the what to do next.
                """,
            ),
            MessagesPlaceholder(variable_name=MEMORY_KEY),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    chat_history = []

    tools = [process_query]
    llm_with_tools = llm.bind(functions=[convert_to_openai_function(t) for t in tools])

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(
                x["intermediate_steps"]
            ),
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    cl.user_session.set("chat_history", chat_history)
    cl.user_session.set("agent", agent_executor)


@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="Smart",
            markdown_description="Slower but more capable.",
            icon="https://picsum.photos/200",
        ),
        cl.ChatProfile(
            name="Basic",
            markdown_description="Fast and returns only direct results.",
            icon="https://picsum.photos/250",
        ),
    ]


@cl.on_chat_start
async def on_chat_start():
    files = None
    while files == None:
        files = await cl.AskFileMessage(
            content="Please select the profile you want to use then upload a zip file of your network snapshot.",
            accept=["application/zip"],
            max_size_mb=20,
            timeout=280,
        ).send()

    file = files[0]

    msg = cl.Message(content="Processing network snapshot...", disable_feedback=True)
    await msg.send()
    
    await cl.make_async(init_batfish)(file.path)
    
    await cl.make_async(init_chains)()

    status = await cl.make_async(generate_parsing_status)()
    
    indication_msg = ""
    if not cl.user_session.get("chat_profile") == "Basic":
        await cl.make_async(init_agent)()
        indication_msg = _agent_suffix.format(profile=cl.user_session.get("chat_profile"))
    else:
        indication_msg = _basic_suffix
        
    msg.content = f"""## Network loaded 🚀

{status}"""
        
    await msg.update()

    msg = cl.Message(content=indication_msg, disable_feedback=True)
    await msg.send()


@cl.on_message
async def on_message(message: cl.Message):
    if not cl.user_session.get("chat_profile") == "Basic":
        chat_history = cl.user_session.get("chat_history")
        agent = cl.user_session.get("agent")
        res = await agent.ainvoke(
            {"input": message.content, "chat_history": chat_history}, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True)]
        )
        await cl.Message(content=res['output']).send()

        chat_history.extend(
            [
                HumanMessage(content=message.content),
                AIMessage(content=res["output"]),
            ]
        )
        cl.user_session.set("chat_history", chat_history)
    else:
        await run_basic(message)
        

async def run_basic(message: cl.Message):
    msg = message.content
    if msg.startswith("/ask"):
        task = msg[len("/ask"):].strip()
        res = ask_chain.invoke(task)
        await cl.Message(content=res).send()
    else:
        res = process_query(msg)
        await cl.Message(content=res).send()
