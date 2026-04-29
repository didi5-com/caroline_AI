"""Runtime settings and path helpers for dev + PyInstaller builds."""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv



def get_base_path() -> Path:
    """Resolve application base path for source and bundled (.exe) execution."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    return Path(__file__).resolve().parent.parent


def resource_path(*parts: str) -> Path:
    return get_base_path().joinpath(*parts)


def writable_data_path(*parts: str) -> Path:
    """Writable data directory for runtime artifacts."""
    base = Path.home() / ".caroline_ai"
    base.mkdir(parents=True, exist_ok=True)
    path = base.joinpath(*parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


# Load .env from project root if available.
load_dotenv(resource_path(".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ZAPIER_WEBHOOK_URL = os.getenv("ZAPIER_WEBHOOK_URL")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
