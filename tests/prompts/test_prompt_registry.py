import pytest

from ai_agent.prompts.prompt_registry import create_registry


def test_retrieve_registered_prompt():
    registry = create_registry()

    prompt = registry.get(
        name="ticket_classification",
        version="1.0.0",
    )

    assert prompt.name == "ticket_classification"
    assert prompt.version == "1.0.0"


def test_retrieve_unknown_prompt():
    registry = create_registry()

    with pytest.raises(ValueError, match="Prompt not found"):
        registry.get(
            name="unknown",
            version="1.0.0",
        )
