from ai_agent.prompts.prompt_template import PromptTemplate
from ai_agent.prompts.ticket_prompts import (
    TICKET_CLASSIFICATION_V1,
    TICKET_CLASSIFICATION_V2,
)


class PromptRegistry:
    def __init__(self) -> None:
        self._prompts: dict[str, PromptTemplate] = {}

    def register(self, prompt: PromptTemplate) -> None:
        key = f"{prompt.name}:{prompt.version}"

        if key in self._prompts:
            raise ValueError(f"Prompt already registered: {key}")

        self._prompts[key] = prompt

    def get(self, name: str, version: str) -> PromptTemplate:
        key = f"{name}:{version}"

        if key not in self._prompts:
            raise ValueError(f"Prompt not found: {key}")

        return self._prompts[key]


def create_registry() -> PromptRegistry:
    registry = PromptRegistry()

    registry.register(TICKET_CLASSIFICATION_V1)
    registry.register(TICKET_CLASSIFICATION_V2)

    return registry
