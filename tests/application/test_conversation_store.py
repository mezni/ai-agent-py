from ai_agent.application.conversation_store import ConversationStore
from ai_agent.domain.conversation import (
    Conversation,
    ConversationMemory,
    Message,
    MessageRole,
)


def test_conversation_messages_persist(tmp_path):
    db = tmp_path / "test.db"

    store = ConversationStore(str(db))

    conversation = Conversation()
    store.create_conversation(conversation)

    message = Message(
        role=MessageRole.USER,
        content="My order #4821 has not arrived.",
    )

    store.add_message(conversation.id, message)

    # Create a new store to simulate application restart.
    new_store = ConversationStore(str(db))

    history = new_store.get_messages(conversation.id)

    assert len(history) == 1
    assert history[0].content == message.content
    assert history[0].role == MessageRole.USER


def test_memory_persists(tmp_path):
    store = ConversationStore(str(tmp_path / "test.db"))

    conversation = Conversation()
    store.create_conversation(conversation)

    memory = ConversationMemory(
        summary="Customer has an undelivered order.",
        facts=["Order ID: 4821"],
    )

    store.save_memory(conversation.id, memory)

    result = store.get_memory(conversation.id)

    assert result.summary == memory.summary
    assert result.facts == memory.facts
