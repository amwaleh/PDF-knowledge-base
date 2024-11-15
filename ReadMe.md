# Introduction 

This is a simple project that connects to an LLM (AzureOpenAi) and incorporates context-specific information from a PDF. As a result, the Bot can answer questions related to the information in the PDF.



# Set up your Model
You can use most of the available models as of October 2023. In this Model we are going to use AzureOpenAI for our models.

## Deploy Model on Azure Ai Studio 
- Deploy a model for chat completion, in this instance we will be using `gpt-4` as this is one of the latest offerings. Choose one that suits you

- Deploy an embedding model, I will be deploying `text-embedding-ada-002`. ensure the embedding model is compatible with your chat model.

- [How to deploy mode in Azure](https://learn.microsoft.com/en-us/azure/ai-studio/quickstarts/get-started-playground)

# Create your python project
- Select a vector database that you will use and set it up. We shall  use [Chromadb](https://docs.trychroma.com/getting-started) for this example 
- If you choose to use Postgres as a vector database you will need to install the vector extension. [check installation instructions here](#postgress-pgvector-extension-installation)
- Setup your virtual environment 


## Set your environment variables 
Add the following environment variables to your system. 

We shall be using `dotenv` package which allows us to declare environment variables in a `.env` file
```js
# .env

AZURE_OPENAI_API_KEY=942f994***********
AZURE_OPENAI_ENDPOINT=https://********.openai.azure.com/
AZURE_OPENAI_API_VERSION=2023-12-01
AZURE_OPENAI_DEPLOYMENT_NAME=mygpt-4
AZURE_EMBEDDING_MODEL_NAME=text-embedding-ada-002

# Telegram config
BOT_TOKEN=800***545:A**********mcaoM
```


## Install dependencies 

```js
python-dotenv
phidata
sqlalchemy
langchain_community
langchain_openai
langchain-chroma>=0.1.2
python-telegram-bot
```

--------------------------------------------------
## Phidata 
[Phidata](https://docs.phidata.com/agents) is an agent framework that will help us build agents connect to the LLM and be able to output the response in a human friendly manner. it abstracts most of the heavy lifting and gives us simple interface to work with. 



### Agents
Phidata uses [agent](https://github.com/phidatahq/phidata) carry out tasks, this agents utilize LLM, various tools, Memory and knowledge base to enhance the A.I experience 

### Vector Database
Vector databases enable us to store information as embeddings and search for “results similar” to our input query using cosine similarity or full text search. These results are then provided to the Agent as context so it can respond in a context-aware manner using Retrieval Augmented Generation (RAG).

In our example we shall be using `ChromaDb`. You can choose any other [vector databases](https://docs.phidata.com/vectordb/introduction) supported by phidata

## Create Knowledge Base

A Knowledge Base is a corpus of information that we want to make our LLM aware of. This specialized information will make the LLM context-aware and thus improve the LLM's response and user experience. This information can be in the form of text, PDFs, databases, JSON, websites, etc.

The information needs to be converted into a format that the LLM can easily interpret. We will need to chunk the information, then convert the chunks into embeddings, before we store the embeddings into a vector database.

```mermaid
flowchart LR
    A[Context Data] --> B[Chunk Information]
    B --> C[Convert Chunks into Embeddings]
    C --> D[Store Embeddings into Vector Database]
    style A fill:#333,stroke:#333,stroke-width:4px,color:fff;
    style B fill:#33f,stroke:#333,stroke-width:2px,color:fff;
    style C fill:#223,stroke:#333,stroke-width:2px,color:fff;
    style D fill:#0A0,stroke:#333,stroke-width:2px,color:fff;
```


-------------------------------------------------
### Why I Chose Langchain PDF Loader

Phidata supports the use of LangChain retriever or vector store as a knowledge base through the LangChainKnowledgeBase agent.

Reasons for this choice:
- Encountered issues with SQLAlchemy while trying to save multiple files.
- Easy functionality for reading files from a directory.

You can also use [PDFKnowledgeBase](https://docs.phidata.com/knowledge/pdf).

## Loading the Vector Store

You only need to run the Knowledge Base Load command once or when updating the information. The `load_vector_store` command should only be run once as the embeddings will be persisted in the VectorDB.

```python
# [main.py](http://_vscodecontentref_/1)

def load_vector_store():
    # Store embeddings into vector store
    loader = PyPDFDirectoryLoader(file_path)
    docs = loader.load()
    Chroma.from_documents(
        .....
    )
```
# Run the app
Run the following command only on the first run:
`python main.py`

On subsequent runs, please comment out the `load_vector_store()` command in the `main.py` file to avoid recreating the vector database.

# Telegram Bot
Install Telegram for [desktop](https://desktop.telegram.org/).

Follow this [guide](https://sendpulse.com/knowledge-base/chatbot/telegram/create-telegram-chatbot) to register a bot.

- Add the Chatbot Key to your environment variables:

```python
AZURE_OPENAI_DEPLOYMENT_NAME=mygpt-4
AZURE_EMBEDDING_MODEL_NAME=text-embedding-ada-002

# Telegram config
BOT_TOKEN=800***545:A**********mcaoM
```

## running your Bot
Run 

`python telegram_bot.py`

start charting with your bot

-----------------------------------



# PgVector installation issues on Windows 
## Postgress pgVector Extension Installation

[pgvector](https://github.com/pgvector/pgvector)

Please check the github page for instruction
- ensure you have latest posgresQL installed that supports Vector extension 
- for windows you will need to have Visual studio installed for you to build the extension
- check the `nmake` executable in visual studio folder 
- Running your console as Administrator, run the make command by referencing the whole path to the nmake file e.g

```Bash 
"C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC\14.41.34120\bin\Hostx64\x64\nmake.exe" /F Makefile.win install

```
NB: change the path to your Visual studio version

- AFter installing  the Extension run the following command in your psql command interface 

```SQL 
CREATE EXTENSION vector;


```








######  *** Information on the PDF is only for demonstration purposes and should not be used as official documentation from any company or individual.