from fastapi import APIRouter, Query

from core.brain import Brain

router = APIRouter()
brain = Brain()


@router.get("/{user_id}")
def get_memory(user_id: str, limit: int = Query(default=10, ge=1, le=100)) -> dict:
    return brain.memory(user_id=user_id, limit=limit)
