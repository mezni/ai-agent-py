import json
from typing import Any

import httpx

from ai_agent_py.application.interfaces.llm_service import (
    LlmRequest,
    LlmResponse,
    LlmService,
)
from ai_agent_py.infrastructure.llm.config import LlmConfig
from ai_agent_py.infrastructure.llm.errors import (
    LlmProviderError,
    LlmResponseError,
)


class OpenAICompatibleLlmAdapter(LlmService):
    def __init__(
        self,
        config: LlmConfig,
        *,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._config = config
        self._transport = transport

    def generate(self, request: LlmRequest) -> LlmResponse:
        payload = {
            "model": self._config.model,
            "messages": [
                {"role": message.role, "content": message.content} for message in request.messages
            ],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }

        try:
            with httpx.Client(
                timeout=self._config.timeout_seconds,
                transport=self._transport,
            ) as client:
                response = client.post(
                    f"{self._config.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self._config.api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )
                response.raise_for_status()

        except httpx.HTTPError as exc:
            raise LlmProviderError("LLM provider request failed.") from exc

        try:
            data: dict[str, Any] = response.json()
            content = data["choices"][0]["message"]["content"]
            model = data.get("model", self._config.model)
            usage = data.get("usage", {})

            if not isinstance(content, str):
                raise TypeError("Expected message content to be a string.")

            return LlmResponse(
                content=content,
                model=model,
                input_tokens=usage.get("prompt_tokens"),
                output_tokens=usage.get("completion_tokens"),
            )

        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise LlmResponseError("LLM provider returned an invalid response.") from exc

    @staticmethod
    def parse_json_object(content: str) -> dict[str, Any]:
        """Parse model output as a JSON object; reject other JSON types."""
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise LlmResponseError("LLM output was not valid JSON.") from exc

        if not isinstance(parsed, dict):
            raise LlmResponseError("LLM JSON output must be an object.")

        return parsed
