import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenRouter Configuration (for free models)
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "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")
    use_openrouter: bool = os.getenv("USE_OPENROUTER", "true").lower() == "true"
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "xiaomi/mimo-v2-flash:free")
    openrouter_api_base: str = "https://openrouter.ai/api/v1"
    
    # OpenAI Configuration (fallback)
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "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")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    
    # Cohere Configuration
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "L6Lp5FaT7aKM3pJDgcHYVhO04zY20Qf0pFrSnVqP")
    embedding_provider: str = os.getenv("EMBEDDING_PROVIDER", "local")  # openai, cohere, or local
    
    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./robotics_book.db")
    
    # Qdrant Configuration
    qdrant_url: str = os.getenv("QDRANT_URL", "https://87e6cee6-c34b-48b0-b267-a780eb956a55.europe-west3-0.gcp.cloud.qdrant.io:6333")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.pGh1v8OU3UVWfNuL9BpCtQHnHRqLRL9nCf5dQcf1t4I")
    qdrant_collection_name: str = "robotics-book"
    
    # Server Configuration
    backend_url: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    # Read as raw string to avoid pydantic-settings JSON parsing issues, convert below
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:8000,http://127.0.0.1:3000,http://127.0.0.1:3001,http://127.0.0.1:8000")
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

# Convert comma-separated CORS string into a Python list for runtime use
try:
    settings.cors_origins = [s.strip() for s in settings.cors_origins.split(",") if s.strip()]
except Exception:
    settings.cors_origins = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8000"
    ]
