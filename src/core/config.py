from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    app_name: str = "Empathy API"
    debug: bool = False

    # LLM Configuration (Google Gemini)
    gemini_api_key: str = ""
    gemini_model: str = "models/gemini-1.5-flash"

    # Cache Configuration
    cache_ttl_seconds: int = 86400  # 24 hours
    cache_max_size: int = 1000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Cached settings loader."""
    return Settings()
