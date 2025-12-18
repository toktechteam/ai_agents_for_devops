from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "runbooks"

    # Small + popular; good quality; downloads on first run.
    embed_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    class Config:
        env_prefix = ""
        case_sensitive = False


settings = Settings()