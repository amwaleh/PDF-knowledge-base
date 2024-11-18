from phi.knowledge.website import WebsiteKnowledgeBase
from phi.vectordb.pgvector import PgVector
from phi.vectordb.chroma import ChromaDb
from phi.agent import Agent
from dotenv import load_dotenv
from azure_model import azure_model
from phi.embedder.azure_openai import AzureOpenAIEmbedder
load_dotenv()
from phi.knowledge.json import JSONKnowledgeBase
from phi.document.reader.json import JSONReader
from phi.knowledge.pdf import PDFUrlKnowledgeBase
import httpx
import json
from medicalTools import MedicalTools
from medical import CustomMedicalKnowledgeBase

def function_get_Bupa_provider(country_code:str = "KE"):
    """
     Get Bupa providers by country code
     args:
        country_code (str): Alpha-2 code of the country e.g AO = Angola, KE = Kenya, UG = Uganda
    return: json response of the Bupa providers
    Save the output in the knowledge base
     """
    url = f"https://www.bupaglobal.com/FacilitiesFinder/GetFacilityByCountry/{country_code}"

    response = httpx.get(url)
    result = response.json()
    print(result)
    return json.dumps(result)


knowledge_base = WebsiteKnowledgeBase(
    model=azure_model,
    urls=["https://www.bupaglobal.com/FacilitiesFinder/GetFacilityByCountry/KE"],
    # Number of links to follow from the seed URLs
    max_links=1,
    # Table name: ai.website_documents
    vector_db=PgVector(
        embedder=AzureOpenAIEmbedder(
           
        ),
        table_name="website_documents",
        db_url="postgresql+psycopg://postgres:postgres@localhost:5433/postgres",
    ),
)

custom_knowledge_base = CustomMedicalKnowledgeBase(countries=["KE"], 
        vector_db=ChromaDb(
            collection="bupa_provider",
        embedder=AzureOpenAIEmbedder(
           
        ),
    ),)

agent = Agent(
    tools=[function_get_Bupa_provider],
    model=azure_model,
    knowledge_base=knowledge_base,
    search_knowledge=True,
    update_knowledge=True,
    # Add a tool to read chat history.
    read_chat_history=True,
    show_tool_calls=True,
    monitoring=True,
)
# agent.knowledge.load(upsert=True)

agent.print_response("how much is the bupa DEntal cover")

# print(get_Bupa_provider())