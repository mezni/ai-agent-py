from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LlmMessage:
    role: str
    content: str


@dataclass(frozen=True)
class LlmRequest:
    messages: list[LlmMessage]
    temperature: float = 0.0
    max_tokens: int = 800


@dataclass(frozen=True)
class LlmResponse:
    content: str
    model: str
    input_tokens: int | None = None
    output_tokens: int | None = None


class LlmService(Protocol):
    def generate(self, request: LlmRequest) -> LlmResponse:
        """Generate a model response for the supplied messages."""
