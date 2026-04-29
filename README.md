# AI Brain System

A modular, backend-first AI assistant foundation designed for desktop/mobile/API clients.

## Project Structure

```text
ai_brain_system/
├── core/
│   ├── __init__.py
│   ├── brain.py
│   ├── agent.py
│   └── reasoning.py
├── memory/
│   ├── __init__.py
│   ├── short_term.py
│   ├── long_term.py
│   └── vector_store.py
├── tools/
│   ├── __init__.py
│   ├── system_tools.py
│   ├── file_tools.py
│   ├── web_tools.py
│   └── zapier_tools.py
├── integrations/
│   ├── __init__.py
│   ├── zapier.py
│   ├── appaca.py
│   └── taskade.py
├── perception/
│   ├── __init__.py
│   ├── speech_to_text.py
│   └── text_to_speech.py
├── api/
│   ├── __init__.py
│   ├── server.py
│   └── routes/
│       ├── __init__.py
│       ├── chat.py
│       ├── memory.py
│       └── actions.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── prompts.py
├── data/
│   ├── memory.db
│   └── logs/
└── tests/
    └── __init__.py
```

## Features

- Conversational orchestration with intent-first processing.
- Short-term (session) + long-term (SQLite) memory.
- Semantic retrieval via vector store abstraction.
- Tool execution framework with Zapier webhook automation.
- FastAPI endpoints for chat, memory, and actions.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ai_brain_system/main.py
```

## API

- `POST /chat`
- `GET /memory/{session_id}`
- `POST /actions/zapier`
- `GET /health`

Set `AI_BRAIN_ZAPIER_WEBHOOK_URL` in `.env` to enable default Zapier webhook dispatch.
