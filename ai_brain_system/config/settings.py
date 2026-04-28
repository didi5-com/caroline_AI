"""Application settings for AI Brain System."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven settings object."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="AI_BRAIN_")

    app_name: str = "AI Brain System"
    app_version: str = "0.1.0"
    debug: bool = False

    data_dir: Path = Path("ai_brain_system/data")
    sqlite_path: Path = Path("ai_brain_system/data/memory.db")

    openai_api_key: str | None = None
    default_model: str = "gpt-4o-mini"

    zapier_webhook_url: str | None = Field(default=None, description="Default Zapier hook")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return singleton settings instance."""
    return Settings()
