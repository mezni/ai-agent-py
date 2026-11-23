from ai_agent.application.ticket_memory_extractor import (
    TicketMemoryExtractor,
)
from ai_agent.domain.conversation import Message, MessageRole


def test_extract_order_id():
    extractor = TicketMemoryExtractor()

    messages = [
        Message(
            role=MessageRole.USER,
            content="My order #4821 has not arrived.",
        )
    ]

    facts = extractor.extract(messages)

    result = {fact.key: fact.value for fact in facts}

    assert result["order_id"] == "4821"
    assert result["issue"] == "order_not_delivered"


def test_extract_email_preference():
    extractor = TicketMemoryExtractor()

    messages = [
        Message(
            role=MessageRole.USER,
            content="I prefer email updates.",
        )
    ]

    facts = extractor.extract(messages)

    assert any(
        fact.key == "communication_preference" and fact.value == "email"
        for fact in facts
    )
