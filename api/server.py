from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.actions import router as actions_router
from api.routes.chat import router as chat_router
from api.routes.memory import router as memory_router

app = FastAPI(title="Caroline AI Brain")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(chat_router, prefix="/chat")
app.include_router(memory_router, prefix="/memory")
app.include_router(actions_router, prefix="/actions")


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "Caroline AI running"}
