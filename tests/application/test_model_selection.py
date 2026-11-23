import pytest

from ai_agent.application.model_registry import (
    ModelRegistry,
)
from ai_agent.application.model_selection import (
    ModelSelector,
)
from ai_agent.domain.model_definition import (
    ModelDefinition,
)


def test_select_model_for_classification():
    registry = ModelRegistry()

    registry.register(
        ModelDefinition(
            name="fast-model",
            provider="openai",
            model_id="test-fast",
            supports_streaming=True,
            supports_tool_calling=True,
            supports_structured_output=True,
            context_window=100000,
        )
    )

    selector = ModelSelector(registry)

    selected = selector.select_for_task(
        "classification"
    )

    assert selected.model_id == "test-fast"


def test_unknown_task_raises_error():
    selector = ModelSelector(ModelRegistry())

    with pytest.raises(ValueError):
        selector.select_for_task("unknown-task")
