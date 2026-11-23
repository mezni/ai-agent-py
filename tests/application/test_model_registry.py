import pytest

from ai_agent.application.model_registry import (
    ModelRegistry,
)
from ai_agent.domain.model_definition import (
    ModelDefinition,
)


def create_model(name: str) -> ModelDefinition:
    return ModelDefinition(
        name=name,
        provider="openai",
        model_id=f"test-{name}",
        supports_streaming=True,
        supports_tool_calling=True,
        supports_structured_output=True,
        context_window=100000,
    )


def test_register_and_get_model():
    registry = ModelRegistry()
    model = create_model("fast-model")

    registry.register(model)

    assert registry.get("fast-model") == model


def test_reject_duplicate_model():
    registry = ModelRegistry()

    registry.register(create_model("fast-model"))

    with pytest.raises(ValueError):
        registry.register(create_model("fast-model"))


def test_unknown_model_raises_error():
    registry = ModelRegistry()

    with pytest.raises(ValueError):
        registry.get("unknown-model")


def test_list_models():
    registry = ModelRegistry()

    registry.register(create_model("fast-model"))
    registry.register(create_model("advanced-model"))

    assert len(registry.list_models()) == 2
