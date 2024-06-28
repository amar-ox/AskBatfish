# AskBatfish: Chat-based Network Management and Verification

AskBatfish allows you to interact with [Batfish](https://github.com/batfish/batfish) through natural language Q&A using Large Language Models (LLMs). It provides a Chatbot UI built with Chainlit and integrates LLMs via LangChain, with persistence handled by Neo4j.

## Getting Started

### Prerequisites

1. **Create a `.env` File**: Generate this file based on the `env.example` template.
   
   > **Note**: The chatbot uses `gpt-4o`. You need to generate an OpenAI API key and configure it in the `.env` file.

2. **Environment Variables**:

    | Variable Name          | Default Value                    | Description                                      |
    |------------------------|----------------------------------|--------------------------------------------------|
    | OPENAI_API_KEY         | None                             | **REQUIRED** - Your OpenAI API key               | 
    | NEO4J_URI              | neo4j://neo4j:7687               | **REQUIRED** - URL to Neo4j database             |
    | NEO4J_USERNAME         | neo4j                            | **REQUIRED** - Username for Neo4j database       |
    | NEO4J_PASSWORD         | 12345-password                   | **REQUIRED** - Password for Neo4j database       |

### Running AskBatfish

1. **Build and Start** (If first time or changes have been made):
    ```sh
    cd chatbot/
    docker compose up --build
    ```

2. **Start**:
    ```sh
    cd chatbot/
    docker compose up
    ```

3. **Watch Mode** (Auto-rebuild on file changes):
    - First, start everything.
    - Then, in a new terminal:
    ```sh
    cd chatbot/
    docker compose watch
    ```

### Using AskBatfish

The chatbot UI will prompt you to upload a snapshot of your network in `.zip` format. If you are unfamiliar with Batfish, refer to [this page](https://pybatfish.readthedocs.io/en/latest/notebooks/interacting.html#Packaging-snapshot-data) to learn how to package your network snapshot configuration files.

Example network snapshots are available in the `/networks` directory for you to experiment with.

#### Modes of Operation

AskBatfish offers two modes:
1. **Agent Mode**: This mode includes an agent that can interpret results and provide detailed explanations.
2. **Basic Mode**: This mode returns raw results directly from Batfish, preferred by engineers who need to see direct results.

In Basic Mode, users can prefix their queries with `/ask` to get help formulating their questions. This feature guides users in providing the necessary details for accurate responses.


### Shutting Down

If health checks fail or containers do not start as expected, shut down completely before starting up again:
```sh
docker compose down
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact

For any questions or concerns regarding this project, please feel free to contact us at: `amaroxmo <at> gmail <dot> com`.
