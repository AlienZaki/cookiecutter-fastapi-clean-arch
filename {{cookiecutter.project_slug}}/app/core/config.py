from typing import Annotated

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    debug: Annotated[
        bool,
        Field(
            description=(
                "Enable debug mode. When enabled, FastAPI runs in debug mode, "
                "uvicorn enables auto-reload, and logging level is set to DEBUG."
            ),
        ),
    ] = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
