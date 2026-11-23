from dataclasses import dataclass


@dataclass(frozen=True)
class GenerationConfig:
    temperature: float | None = None
    top_p: float | None = None
    max_output_tokens: int = 500
    frequency_penalty: float | None = None
    presence_penalty: float | None = None
