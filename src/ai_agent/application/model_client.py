from typing import Protocol

from ai_agent.domain.models import ModelRequest, ModelResponse


class ModelClient(Protocol):
    def generate(self, request: ModelRequest) -> ModelResponse: ...
