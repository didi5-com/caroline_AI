"""Chat endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ai_brain_system.api.dependencies import get_brain
from ai_brain_system.core.brain import AIBrain

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    session_id: str
    message: str


@router.post("")
def chat(payload: ChatRequest, brain: AIBrain = Depends(get_brain)) -> dict:
    return brain.process(session_id=payload.session_id, user_input=payload.message)
