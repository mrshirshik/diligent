from typing import List
import os

# Try to import BaseSettings from the correct location
try:
    from pydantic_settings import BaseSettings  # type: ignore[import]
except ImportError:
    from pydantic import BaseSettings  # type: ignore[attr-defined]


class Settings(BaseSettings):  # type: ignore[misc]
    # Pinecone
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    pinecone_environment: str = os.getenv("PINECONE_ENVIRONMENT", "us-east-1-aws")
    pinecone_index_name: str = os.getenv("PINECONE_INDEX_NAME", "jarvis-index")

    # LLM Configuration
    llm_model_path: str = os.getenv("LLM_MODEL_PATH", os.path.join(os.path.dirname(__file__), "models/llama-2-7b-chat.Q4_K_M.gguf"))
    llm_context_window: int = int(os.getenv("LLM_CONTEXT_WINDOW", "2048"))
    llm_max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "512"))
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))

    # Embedding Model
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"]

    # Database
    knowledge_base_path: str = os.getenv("KNOWLEDGE_BASE_PATH", "./data/knowledge_base.json")

    class Config:
        env_file = ".env"


settings = Settings()
