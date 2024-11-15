
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
        "Use the Bupa policy and provider list inside the knowledge base to anser user query.",
        "Use the Bupa policy and SSN list only when query is related to health insurance",
        "any other query decline to answer politely",
        "provide citation, page number, document name where possible",
        "add date of when the policy was created when cautioning the user on relevance of the information",
        "for SSN list do a thorough search on this fields  Name, Type, Address, City, Contact Information"
    ]

def load_vector_store():
    # Store embeddigs into vectorstore
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
    retriever = db.as_retriever( )

    # Create a knowledgebase from the vector store
    knowledge_base = LangChainKnowledgeBase(
        retriever=retriever, 
        num_documents=20)
    
    agent = Agent(
        knowledge_base=knowledge_base, 
        add_references_to_prompt=True, 
        model=azure_model,
        storage=SqlAgentStorage(table_name="Bupa_gent", db_file="agents.db"),
        add_history_to_messages=True,
        instructions=instructions,
        markdown=True
        )
    
    return agent.run(query)

if __name__ == "__main__":
    
    load_vector_store() # comment this line if you have already loaded the vector store
    print("Vector store loaded, proceeding to test connection ...")
    get_bupa_knowledge("what maximum sum each offer for this insurance types policy?")
