from google import genai
from google.genai import types
import time
import os
import re
import mimetypes
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

store_name = os.getenv('STORE_NAME')

client = genai.Client()

client.file_search_stores.delete(name='fileSearchStores/lincolnrag-sfqi2owz6ifq')

# File name will be visible in citations
file_search_store = client.file_search_stores.create(config={'display_name': 'lincoln_rag'})


for store in client.file_search_stores.list():
    print(store.name, store.display_name, store.active_documents_count)
