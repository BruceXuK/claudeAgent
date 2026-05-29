import os

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# Local embeddings model (free, no API key needed)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Chroma vector store
CHROMA_DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")

# RAG chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

MAX_REACT_ROUNDS = 8
