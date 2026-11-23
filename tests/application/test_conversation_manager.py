from ai_agent.application.context_manager import ContextManager
from ai_agent.application.conversation_manager import (
    ConversationManager,
)
from ai_agent.application.conversation_store import ConversationStore


def test_conversation_manager(tmp_path):
    store = ConversationStore(str(tmp_path / "test.db"))

    manager = ConversationManager(
        store=store,
        context_manager=ContextManager(),
    )

    conversation_id = manager.start_conversation()

    manager.add_user_message(
        conversation_id,
        "My order #4821 has not arrived.",
    )

    manager.add_assistant_message(
        conversation_id,
        "I can help investigate order #4821.",
    )

    context = manager.build_context(
        conversation_id=conversation_id,
        system_prompt="You are a support assistant.",
        current_message="Can you check its status?",
    )

    assert context[-1]["content"] == "Can you check its status?"
    assert any("4821" in message["content"] for message in context)
