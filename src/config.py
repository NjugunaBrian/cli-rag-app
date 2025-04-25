import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

#Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "text-embedding-ada-002"
LLM_MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0
VECTOR_DB_PATH = "./embeddings/chroma_db"
DATA_PATH = "./data"

