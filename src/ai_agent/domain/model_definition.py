from dataclasses import dataclass


@dataclass(frozen=True)
class ModelDefinition:
    name: str
    provider: str
    model_id: str
    supports_streaming: bool
    supports_tool_calling: bool
    supports_structured_output: bool
    context_window: int
