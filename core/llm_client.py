"""Safe OpenAI client initialization helpers."""
from __future__ import annotations

from typing import Any

from config.settings import OPENAI_API_KEY


def get_openai_client() -> Any | None:
    if not OPENAI_API_KEY:
        return None

    try:
        from openai import OpenAI  # local import for PyInstaller friendliness

        return OpenAI(api_key=OPENAI_API_KEY)
    except Exception:
        return None
