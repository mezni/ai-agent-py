from ai_agent.domain.model_definition import (
    ModelDefinition,
)


class ModelRegistry:
    def __init__(self) -> None:
        self._models: dict[str, ModelDefinition] = {}

    def register(self, model: ModelDefinition) -> None:
        if model.name in self._models:
            raise ValueError(
                f"Model already registered: {model.name}"
            )

        self._models[model.name] = model

    def get(self, name: str) -> ModelDefinition:
        try:
            return self._models[name]
        except KeyError:
            raise ValueError(
                f"Unknown model: {name}"
            ) from None

    def list_models(self) -> list[ModelDefinition]:
        return list(self._models.values())
