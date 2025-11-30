import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Paths
    PDF_PATH = "data/qatar_test_doc.pdf"
    
    # Chunking
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    
    # Embedding - USE OPENAI (no memory issues)
    USE_OPENAI_EMBEDDINGS = True  # Changed to True
    EMBEDDING_MODEL = "text-embedding-3-small"
    
    # LLM
    LLM_MODEL = "gpt-3.5-turbo"
    LLM_TEMPERATURE = 0.1
    
    # Retrieval
    TOP_K = 5
    USE_RERANKING = False