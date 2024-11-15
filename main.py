from phi.agent import Agent
from phi.knowledge.langchain import LangChainKnowledgeBase
from phi.storage.agent.sqlite import SqlAgentStorage

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_openai import AzureOpenAIEmbeddings
from langchain_chroma import Chroma

from azure_model import azure_model

chroma_db_dir = "./chroma_db"
file_path = "./knowledgebase"

instructions = [
    "Use the Bupa policy and provider list inside the knowledge base to answer user queries.",
    "Use the Bupa policy and SSN list only when the query is related to health insurance.",
    "For any other query, decline and answer politely.",
    "Provide citation, page number, and document name where possible.",
    "Add the date when the policy was created when cautioning the user on the relevance of the information.",
    "For the SSN list or provider look up, do a thorough search on these fields: Name, Type, Address, City, Contact Information."
]

def load_vector_store():
    # Store embeddings into vector store
    loader = PyPDFDirectoryLoader(file_path)
    docs = loader.load()
    Chroma.from_documents(
        collection_name="bupa_policy",
        documents=docs, 
        embedding=AzureOpenAIEmbeddings(), 
        persist_directory=str(chroma_db_dir),
    )

def get_bupa_knowledge(query):
    db = Chroma(
        embedding_function=AzureOpenAIEmbeddings(), 
        persist_directory=str(chroma_db_dir)
    )
    
    # Create a retriever from the vector store
    retriever = db.as_retriever()

    # Create a knowledge base from the vector store
    knowledge_base = LangChainKnowledgeBase(
        retriever=retriever, 
        num_documents=20
    )
    
    agent = Agent(
        knowledge_base=knowledge_base, 
        add_references_to_prompt=True, 
        model=azure_model,
        storage=SqlAgentStorage(table_name="Bupa_agent", db_file="agents.db"),
        add_history_to_messages=True,
        instructions=instructions,
        markdown=True
    )
    
    return agent.run(query)

if __name__ == "__main__":
    load_vector_store()  # Comment this line if you have already loaded the vector store
    print("Vector store loaded, proceeding to test connection ...")
    get_bupa_knowledge("What is the maximum sum each offer for this insurance type policy?")
