import pytest

from ai_agent.domain.memory import MemoryFact


def test_create_memory_fact():
    fact = MemoryFact(
        key="order_id",
        value="4821",
    )

    assert fact.key == "order_id"
    assert fact.value == "4821"
    assert fact.confidence == 1.0


def test_memory_fact_rejects_empty_key():
    with pytest.raises(ValueError):
        MemoryFact(key="", value="4821")


def test_memory_fact_rejects_invalid_confidence():
    with pytest.raises(ValueError):
        MemoryFact(
            key="order_id",
            value="4821",
            confidence=1.5,
        )
