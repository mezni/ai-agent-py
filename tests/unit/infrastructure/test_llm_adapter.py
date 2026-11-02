import json

import httpx
import pytest

from ai_agent_py.application.interfaces.llm_service import (
    LlmMessage,
    LlmRequest,
)
from ai_agent_py.infrastructure.llm.config import LlmConfig
from ai_agent_py.infrastructure.llm.errors import (
    LlmProviderError,
    LlmResponseError,
)
from ai_agent_py.infrastructure.llm.openai_compatible_adapter import (
    OpenAICompatibleLlmAdapter,
)


@pytest.fixture
def config() -> LlmConfig:
    return LlmConfig(
        base_url="https://llm.example.test/v1",
        api_key="test-key",
        model="test-model",
        timeout_seconds=5,
    )


@pytest.mark.unit
def test_adapter_maps_provider_response(config: LlmConfig) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/chat/completions"
        assert request.headers["Authorization"] == "Bearer test-key"

        payload = json.loads(request.content)
        assert payload["model"] == "test-model"

        return httpx.Response(
            200,
            json={
                "model": "test-model",
                "choices": [{"message": {"content": "Hello from the model."}}],
                "usage": {
                    "prompt_tokens": 12,
                    "completion_tokens": 5,
                },
            },
        )

    transport = httpx.MockTransport(handler)
    adapter = OpenAICompatibleLlmAdapter(config, transport=transport)

    result = adapter.generate(
        LlmRequest(
            messages=[LlmMessage(role="user", content="Hello")],
        )
    )

    assert result.content == "Hello from the model."
    assert result.model == "test-model"
    assert result.input_tokens == 12
    assert result.output_tokens == 5


@pytest.mark.unit
def test_adapter_converts_http_error(config: LlmConfig) -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(429, json={"error": "rate limited"})
    )
    adapter = OpenAICompatibleLlmAdapter(config, transport=transport)

    with pytest.raises(LlmProviderError):
        adapter.generate(
            LlmRequest(
                messages=[LlmMessage(role="user", content="Hello")],
            )
        )


@pytest.mark.unit
def test_adapter_rejects_invalid_provider_response(
    config: LlmConfig,
) -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json={"unexpected": "shape"})
    )
    adapter = OpenAICompatibleLlmAdapter(config, transport=transport)

    with pytest.raises(LlmResponseError):
        adapter.generate(
            LlmRequest(
                messages=[LlmMessage(role="user", content="Hello")],
            )
        )


@pytest.mark.unit
def test_json_parser_accepts_object() -> None:
    result = OpenAICompatibleLlmAdapter.parse_json_object('{"intent": "ORDER_INQUIRY"}')

    assert result == {"intent": "ORDER_INQUIRY"}


@pytest.mark.unit
def test_json_parser_rejects_invalid_json() -> None:
    with pytest.raises(LlmResponseError):
        OpenAICompatibleLlmAdapter.parse_json_object("{not json}")


@pytest.mark.unit
def test_json_parser_rejects_json_array() -> None:
    with pytest.raises(LlmResponseError):
        OpenAICompatibleLlmAdapter.parse_json_object('["value"]')
