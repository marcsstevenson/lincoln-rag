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

def sanitize_resource_name(filename):
    """
    Convert filename to valid resource name format:
    - Only lowercase alphanumeric characters or dashes
    - Cannot begin or end with a dash
    - Maximum 40 characters
    """
    # Convert to lowercase
    name = filename.lower()
    # Replace invalid characters with dashes
    name = re.sub(r'[^a-z0-9-]', '-', name)
    # Remove leading/trailing dashes
    name = name.strip('-')
    # Replace multiple consecutive dashes with single dash
    name = re.sub(r'-+', '-', name)
    # Truncate to 40 characters
    if len(name) > 40:
        name = name[:40]
    # Remove trailing dash if truncation created one
    name = name.rstrip('-')
    return name

print("GOOGLE_API_KEY:", os.environ['GOOGLE_API_KEY'])

client = genai.Client()
target_upload_dir = "C:/Temp/lincoln_rag_uploads"

# File name will be visible in citations
# file_search_store = client.file_search_stores.create(config={'display_name': 'lincoln_rag'})
# file_search_store = client.file_search_stores.delete(name='fileSearchStores/lincolnrag-ngzp18t5xhr2')
file_search_store = client.file_search_stores.get(name=store_name)

# Upload all files in target_upload_dir
# First, get list of existing files in the store

existing_files = set()
for doc in client.file_search_stores.documents.list(parent=store_name):
    existing_files.add(doc.display_name)

print(f"Found {len(existing_files)} existing files in store")

for filename in os.listdir(target_upload_dir):
    file_path = os.path.join(target_upload_dir, filename)

    # Only process files, not directories
    if os.path.isfile(file_path):
        resource_name = sanitize_resource_name(filename)

        # Skip if file already exists in store
        if resource_name in existing_files:
            print(f"Skipping {filename} - already exists in store")
            continue

        print(f"Uploading file from {file_path} with name {resource_name}")

        # Detect MIME type
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type is None:
            mime_type = 'application/octet-stream'

        # Open and read file with explicit encoding handling for Unicode filenames
        with open(file_path, 'rb') as f:
            uploaded_file = client.files.upload(
                file=f,
                config={
                    'name': resource_name,
                    'display_name': filename,
                    'mime_type': mime_type
                }
            )

        operation = client.file_search_stores.import_file(
            file_search_store_name=file_search_store.name,
            file_name=uploaded_file.name
        )

        while not operation.done:
            time.sleep(5)
            operation = client.operations.get(operation)

        print(f"Successfully uploaded and imported {filename}")

for store in client.file_search_stores.list():
    print(store.name, store.display_name, store.active_documents_count)
