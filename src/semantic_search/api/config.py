import os

from dotenv import load_dotenv

load_dotenv()

TYPESENSE_API_KEY: str = os.getenv("TYPESENSE_API_KEY")
TYPESENSE_HOST: str = os.getenv("TYPESENSE_HOST")
TYPESENSE_PORT: str = os.getenv("TYPESENSE_PORT")
TYPESENSE_PROTOCOL: str = os.getenv("TYPESENSE_PROTOCOL")

COLLECTION_NAME: str = os.getenv("COLLECTION_NAME")

SEARCH_ENDPOINT: str = os.getenv("SEARCH_ENDPOINT")
LLM_ENDPOINT: str = os.getenv("LLM_ENDPOINT")

LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3.2")

CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY")