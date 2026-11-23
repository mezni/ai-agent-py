from ai_agent.application.conversation_store import ConversationStore
from ai_agent.domain.memory import MemoryFact


def test_long_term_memory_persistence(tmp_path):
    db = tmp_path / "memory.db"

    store = ConversationStore(str(db))

    store.save_fact(
        "customer-123",
        MemoryFact(
            key="communication_preference",
            value="email",
        ),
    )

    new_store = ConversationStore(str(db))

    facts = new_store.get_facts("customer-123")

    assert len(facts) == 1
    assert facts[0].value == "email"


def test_memory_update_does_not_create_duplicate(tmp_path):
    store = ConversationStore(str(tmp_path / "memory.db"))

    store.save_fact(
        "customer-123",
        MemoryFact("communication_preference", "email"),
    )

    store.save_fact(
        "customer-123",
        MemoryFact("communication_preference", "phone"),
    )

    facts = store.get_facts("customer-123")

    assert len(facts) == 1
    assert facts[0].value == "phone"
