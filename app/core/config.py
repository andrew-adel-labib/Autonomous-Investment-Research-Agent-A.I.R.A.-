import os
from pydantic_settings import BaseSettings, SettingsConfigDict


IS_TEST = bool(os.getenv("PYTEST_CURRENT_TEST")) or os.getenv("ENVIRONMENT") == "test"


class Settings(BaseSettings):
    APP_NAME: str = "AIRA"
    ENVIRONMENT: str = "test" if IS_TEST else os.getenv("ENVIRONMENT", "development")

    DATABASE_URL: str = (
        "sqlite:///./test.db"
        if IS_TEST
        else os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/aira"
        )
    )

    REDIS_URL: str = (
        "redis://localhost:6379/0"
        if IS_TEST
        else os.getenv(
            "REDIS_URL",
            "redis://localhost:6379/0"
        )
    )

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    ALPHA_VANTAGE_KEY: str = os.getenv("ALPHA_VANTAGE_KEY", "")
    MCP_SERVER_URL: str = os.getenv(
        "MCP_SERVER_URL",
        "http://localhost:9000"
    )

    model_config = SettingsConfigDict(
        env_file=None if IS_TEST else ".env",
        extra="ignore"
    )


settings = Settings()