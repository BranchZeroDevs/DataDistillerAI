"""Configuration settings for DataDistillerAI."""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class Settings:
    """Application settings."""
    
    # API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Paths
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vector_store")
    DATA_PATH = os.getenv("DATA_PATH", "./data")
    
    # LLM Parameters
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "500"))
    
    # Embedding Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # Processing Parameters
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1024"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "128"))
    MIN_CHUNK_LENGTH = int(os.getenv("MIN_CHUNK_LENGTH", "100"))
    
    # Retrieval Parameters
    TOP_K_RETRIEVALS = int(os.getenv("TOP_K_RETRIEVALS", "5"))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
