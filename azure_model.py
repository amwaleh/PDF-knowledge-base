import os
from phi.model.azure import AzureOpenAIChat
from rich.console import Console

# from langchain_openai import AzureChatOpenAI


OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")



azure_model = AzureOpenAIChat(
    id="gpt-4-test",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    openai_api_version=os.environ["OPENAI_API_VERSION"],
)



if __name__ == "__main__": 
    console = Console()
    system_message = """I am Daylight, a team-building enthusiast who helps 
    people discover venues with team-building sites and hotels in their area.
      If no area is specified, I will default to nearby hotels or parks. 
      I will provide three suggestions for nearby event locations that vary in activity. 
      I wil provide a price range andfor the hotels, and a picture and a location link.
      I will also share an interesting fact about each site when making a recommendation. 
      The output will be in markdown table format.
     """
    with console.status("Finding a hike for you", spinner="dots") as status:
        
        client = azure_model.get_client()
        response = client.chat.completions.create(
            model="gpt-4-test",
            temperature=0.7,
            max_tokens=400,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": "find me an affordable hotel near nairobi"},
            ]
        )
    generated_text = response.choices[0].message.content

     # Print the response
    print("Response: " + generated_text + "\n")

  