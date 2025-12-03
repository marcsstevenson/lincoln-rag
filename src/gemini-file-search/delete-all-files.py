from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = genai.Client()

print("Deleting all files from client.files")

# Delete all files
deleted_count = 0
for file in client.files.list():
    print(f"Deleting {file.display_name} ({file.name})")
    client.files.delete(name=file.name)
    deleted_count += 1

print(f"Successfully deleted {deleted_count} files")

