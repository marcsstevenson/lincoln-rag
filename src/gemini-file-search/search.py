from google import genai
from google.genai import types
import time
import os
from constants import store_name
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = genai.Client()

questions = [
    "What did the Māori people lose?",
    "what was the venue and date of the Waimate–Taiāmai ki Kaikohe hearing?"
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



