from ai_brain_system.core.brain import AIBrain


def test_brain_conversation_flow() -> None:
    brain = AIBrain()
    result = brain.process(session_id="test-session", user_input="remember this architecture is modular")

    assert result["intent"] in {"memory_store", "conversation"}
    assert isinstance(result["response"], str)
    assert result["stored_memory_id"] is not None


def test_memory_retrieval_flow() -> None:
    brain = AIBrain()
    brain.process(session_id="test-session-2", user_input="save this note for later")

    memory = brain.long_term.fetch_recent("test-session-2", limit=5)
    assert len(memory) >= 1
