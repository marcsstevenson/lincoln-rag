from google import genai
from google.genai import types
import time
import os
import re
import mimetypes
from constants import store_name
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = genai.Client()

client.file_search_stores.delete(name='fileSearchStores/lincolnrag-sfqi2owz6ifq')

# File name will be visible in citations
file_search_store = client.file_search_stores.create(config={'display_name': 'lincoln_rag'})


for store in client.file_search_stores.list():
    print(store.name, store.display_name, store.active_documents_count)
