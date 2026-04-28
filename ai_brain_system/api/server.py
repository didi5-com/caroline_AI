"""FastAPI server setup."""
from __future__ import annotations

from fastapi import FastAPI

from ai_brain_system.api.routes.actions import router as actions_router
from ai_brain_system.api.routes.chat import router as chat_router
from ai_brain_system.api.routes.memory import router as memory_router
from ai_brain_system.config.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.sqlite_path.parent.mkdir(parents=True, exist_ok=True)

    app = FastAPI(title=settings.app_name, version=settings.app_version)
    app.include_router(chat_router)
    app.include_router(memory_router)
    app.include_router(actions_router)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
