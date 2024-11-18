from phi.tools import Toolkit
from phi.utils.log import logger
from typing import List, Optional
import httpx
from phi.document import Document
import json
from medical import CustomMedicalKnowledgeBase
class MedicalTools(Toolkit):
    def __init__(self, knowledge_base:Optional[CustomMedicalKnowledgeBase] = None):
        super().__init__(name="medical_tools")
        self.knowledge_base: Optional[CustomMedicalKnowledgeBase] = knowledge_base
        self.register(self.get_bupa_provider)
    
    def get_bupa_provider(self, country_code:str = "KE"):
     
        """
         Get Bupa providers by country code
         args:
            country_code (str): Alpha-2 code of the country e.g AO = Angola, KE = Kenya, UG = Uganda
        return:
            json: json response of the Bupa providers
         """
       
        # add result to knowledge base
        logger.debug(f"Adding to knowledge base: {country_code}") 
        self.knowledge_base.countries.append(country_code)
        logger.debug("Loading knowledge base hapa.")
        self.knowledge_base.load(upsert=True)
        logger.debug(f"Searching knowledge base: {country_code}")
        relevant_docs: List[Document] = self.knowledge_base.search(query=country_code)
        return json.dumps([doc.to_dict() for doc in relevant_docs])