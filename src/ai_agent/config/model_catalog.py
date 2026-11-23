from ai_agent.domain.model_definition import (
    ModelDefinition,
)
from ai_agent.application.model_registry import (
    ModelRegistry,
)


def build_model_registry() -> ModelRegistry:
    registry = ModelRegistry()

    registry.register(
        ModelDefinition(
            name="fast-model",
            provider="openai",
            model_id="YOUR_FAST_MODEL_ID",
            supports_streaming=True,
            supports_tool_calling=True,
            supports_structured_output=True,
            context_window=0,
        )
    )

    registry.register(
        ModelDefinition(
            name="advanced-model",
            provider="openai",
            model_id="YOUR_ADVANCED_MODEL_ID",
            supports_streaming=True,
            supports_tool_calling=True,
            supports_structured_output=True,
            context_window=0,
        )
    )

    return registry
