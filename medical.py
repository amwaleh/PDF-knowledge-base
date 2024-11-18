from pathlib import Path
from typing import Union, List, Iterator
import logging
import json
import httpx
from phi.document import Document
from phi.document.reader.json import JSONReader
from phi.knowledge.agent import AgentKnowledge

from phi.utils.log import logger
class CustomMedicalKnowledgeBase(AgentKnowledge):
    countries: List[str]
    

    @property
    def document_lists(self) -> Iterator[List[Document]]:
        """Iterate over Json files and yield lists of documents.
        Each object yielded by the iterator is a list of documents.

        Returns:
            Iterator[List[Document]]: Iterator yielding list of documents
        """

        for country in self.countries:
            yield self.retrieve_bupa_provider(country)




    def retrieve_bupa_provider(self, country_code:str = "KE"):
     
        """
         Get Bupa providers by country code
         args:
            country_code (str): Alpha-2 code of the country e.g AO = Angola, KE = Kenya, UG = Uganda
        return:
            json: json response of the Bupa providers
         """
        url = f"https://www.bupaglobal.com/FacilitiesFinder/GetFacilityByCountry/{country_code}"
        
        logger.debug("retrieving info from the web")
        response = httpx.get(url)
        result = response.json()
        # add result to knowledge base 
        if isinstance(result, dict):
            result = [result]
        docunemt= [
            Document(
              
                content=json.dumps(content))
                for page_number, content in enumerate(result, start=1)
            
        ]
        return docunemt