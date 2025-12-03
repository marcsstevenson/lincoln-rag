from google import genai
from google.genai import types
import os
from constants import store_name
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = genai.Client()

# Get the file search store
file_search_store = client.file_search_stores.get(name=store_name)

print(f"Deleting all files from store: {store_name}")

# List all documents in the store and delete them
deleted_count = 0
for doc in client.file_search_stores.documents.list(parent=store_name):
    print(f"Deleting {doc.display_name} ({doc.name})")
    # Delete from the file search
    client.file_search_stores.documents.delete(name=doc.name, config={'force': True})
    # delete the underlying file
    client.files.delete(name=doc.name, config={'force': True})

    deleted_count += 1

print(f"Successfully deleted {deleted_count} files from store")
