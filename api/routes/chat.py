from fastapi import APIRouter
from pydantic import BaseModel

from core.brain import Brain

router = APIRouter()
brain = Brain()


class ChatRequest(BaseModel):
    user_id: str
    message: str


@router.post("/")
def chat(req: ChatRequest) -> dict[str, str]:
    response = brain.process(req.user_id, req.message)
    return {"response": response}
