from __future__ import annotations

import os
import traceback


def run() -> None:
    mode = os.getenv("CAROLINE_MODE", "api").lower()

    if mode == "voice":
        from core.voice_engine import VoiceEngine

        VoiceEngine().run()
        return

    import uvicorn

    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    try:
        run()
    except Exception as exc:  # noqa: BLE001
        print(f"[startup] fatal error: {exc}")
        traceback.print_exc()
        raise SystemExit(1)
