from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from core.brain import Brain

router = APIRouter()
brain = Brain()


class ActionRequest(BaseModel):
    action: str
    payload: dict[str, Any]


@router.post("/")
def run_action(req: ActionRequest) -> dict[str, Any]:
    result = brain.trigger_action(req.action, req.payload)
    return {"result": result}
