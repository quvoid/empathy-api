from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class AppConfig(BaseSettings):
    """
    Centralized application configuration.
    Loads from environment variables and .env file.
    """

    # API Configuration
    APP_NAME: str = "Empathy API"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"

    # LLM Configuration
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash" 

    # Cache Configuration
    CACHE_TTL_SECONDS: int = 86400  # 24 hours
    CACHE_MAX_SIZE: int = 1000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_config() -> AppConfig:
    """Cached configuration factory."""
    return AppConfig()
