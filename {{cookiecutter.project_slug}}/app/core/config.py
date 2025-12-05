import logging

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    debug: bool = False
    log_level: int = logging.INFO

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
