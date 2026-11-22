import pytest

from ai_agent.prompts.prompt_builder import (
    build_ticket_classification_prompt,
)


def test_build_ticket_classification_prompt():
    prompt = build_ticket_classification_prompt("My order #4821 has not arrived.")

    assert "customer support ticket classification" in prompt
    assert "My order #4821 has not arrived." in prompt
    assert "order_status" in prompt


def test_empty_ticket():
    with pytest.raises(ValueError, match="Ticket cannot be empty"):
        build_ticket_classification_prompt(" ")
