import os
from dataclasses import dataclass


@dataclass(frozen=True)
class LlmConfig:
    base_url: str
    api_key: str
    model: str
    timeout_seconds: float = 30.0

    @classmethod
    def from_environment(cls) -> "LlmConfig":
        base_url = os.getenv(
            "LLM_BASE_URL",
            "https://api.openai.com/v1",
        ).rstrip("/")
        api_key = os.getenv("LLM_API_KEY", "")
        model = os.getenv("LLM_MODEL", "")
        timeout_seconds = float(os.getenv("LLM_TIMEOUT_SECONDS", "30"))

        if not api_key:
            raise ValueError("LLM_API_KEY is required.")

        if not model:
            raise ValueError("LLM_MODEL is required.")

        if timeout_seconds <= 0:
            raise ValueError("LLM_TIMEOUT_SECONDS must be positive.")

        return cls(
            base_url=base_url,
            api_key=api_key,
            model=model,
            timeout_seconds=timeout_seconds,
        )
