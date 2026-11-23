from ai_agent.application.model_registry import (
    ModelRegistry,
)
from ai_agent.domain.model_definition import (
    ModelDefinition,
)


class ModelSelector:
    def __init__(
        self,
        registry: ModelRegistry,
    ) -> None:
        self.registry = registry

    def select_for_task(
        self,
        task: str,
    ) -> ModelDefinition:

        task_models = {
            "classification": "fast-model",
            "entity_extraction": "fast-model",
            "complex_reasoning": "advanced-model",
            "customer_response": "advanced-model",
        }

        model_name = task_models.get(task)

        if model_name is None:
            raise ValueError(
                f"No model configured for task: {task}"
            )

        return self.registry.get(model_name)
