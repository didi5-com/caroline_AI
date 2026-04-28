"""Memory endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from ai_brain_system.api.dependencies import get_brain
from ai_brain_system.core.brain import AIBrain

router = APIRouter(prefix="/memory", tags=["memory"])


@router.get("/{session_id}")
def get_memory(
    session_id: str,
    limit: int = Query(default=10, ge=1, le=100),
    brain: AIBrain = Depends(get_brain),
) -> dict:
    return {
        "session_id": session_id,
        "short_term": brain.short_term.get_context(session_id),
        "long_term": brain.long_term.fetch_recent(session_id, limit=limit),
    }
