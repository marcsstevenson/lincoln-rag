from google import genai
from google.genai import types
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

store_name = os.getenv('STORE_NAME')

client = genai.Client()

questions = [
    # "What did the Māori people lose?",
    # "what was the venue and date of the Waimate–Taiāmai ki Kaikohe hearing?",
    # "in the REPORT OF THE WAITANGI TRIBUNAL ON THE MANGONUI SEWERAGE CLAIM (Wai-17), looking at FIGURE 2 - TAIPA, what is the name of the Bay?",
    "in the REPORT OF THE WAITANGI TRIBUNAL ON THE MANGONUI SEWERAGE CLAIM (Wai-17), looking at FIGURE 2 - TAIPA, what is the name of the Creek?",
]

for question in questions:
     response = client.models.generate_content(
         model="gemini-2.5-flash",
         contents=question,
         config=types.GenerateContentConfig(
             tools=[
                 types.Tool(
                     file_search=types.FileSearch(
                         file_search_store_names=[store_name]
                     )
                 )
             ]
         )
     )

     print(f"Q: {question}")
     print(f"A: {response.text}")
     print("-----")



