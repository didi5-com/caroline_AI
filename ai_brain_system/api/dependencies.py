"""Shared API dependencies."""
from __future__ import annotations

from functools import lru_cache

from ai_brain_system.core.brain import AIBrain


@lru_cache(maxsize=1)
def get_brain() -> AIBrain:
    return AIBrain()
