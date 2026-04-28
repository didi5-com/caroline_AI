"""Action/tool execution endpoints."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ai_brain_system.api.dependencies import get_brain
from ai_brain_system.core.brain import AIBrain

router = APIRouter(prefix="/actions", tags=["actions"])


class ZapierActionRequest(BaseModel):
    event_name: str
    data: dict[str, Any]
    webhook_url: str | None = None


@router.post("/zapier")
def trigger_zapier(payload: ZapierActionRequest, brain: AIBrain = Depends(get_brain)) -> dict:
    result = brain.execute_action(
        action_name="zapier",
        payload={
            "event_name": payload.event_name,
            "data": payload.data,
            "webhook_url": payload.webhook_url,
        },
    )
    return {"status": "executed", "result": result}
