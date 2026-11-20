from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import openai
import pytest

from ai_agent.config import settings
from ai_agent.providers.openai_provider import OpenAIProvider, ProviderResponse, Usage


@pytest.fixture
def provider_client():
    with patch("ai_agent.providers.openai_provider.OpenAI") as openai_client:
        provider = OpenAIProvider()
        yield provider, openai_client.return_value


def make_response(output_text="Hello, world!", input_tokens=11, output_tokens=5):
    return SimpleNamespace(
        output_text=output_text,
        usage=SimpleNamespace(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
        ),
    )


def make_status_error(error_class, status_code):
    response = MagicMock(status_code=status_code)
    return error_class("request failed", response=response, body=None)


def test_generate_returns_successful_response_text(provider_client):
    provider, client = provider_client
    client.responses.create.return_value = make_response()

    result = provider.generate("What is the weather?")

    assert result == "Hello, world!"
    client.responses.create.assert_called_once_with(
        model=settings.openai_model,
        instructions="You are a helpful assistant.",
        input="What is the weather?",
    )


def test_generate_raises_authentication_error(provider_client):
    provider, client = provider_client
    error = make_status_error(openai.AuthenticationError, 401)
    client.responses.create.side_effect = error

    with pytest.raises(RuntimeError, match="Provider authentication failed") as exc_info:
        provider.generate("What is the weather?")

    assert exc_info.value.__cause__ is error


def test_generate_raises_connection_error(provider_client):
    provider, client = provider_client
    error = openai.APIConnectionError(request=MagicMock())
    client.responses.create.side_effect = error

    with pytest.raises(RuntimeError, match="Provider connection failed") as exc_info:
        provider.generate("What is the weather?")

    assert exc_info.value.__cause__ is error


def test_generate_raises_api_server_error(provider_client):
    provider, client = provider_client
    error = make_status_error(openai.InternalServerError, 500)
    client.responses.create.side_effect = error

    with pytest.raises(RuntimeError, match="Provider returned HTTP 500") as exc_info:
        provider.generate("What is the weather?")

    assert exc_info.value.__cause__ is error


def test_generate_with_usage_extracts_token_counts(provider_client):
    provider, client = provider_client
    client.responses.create.return_value = make_response(input_tokens=13, output_tokens=7)

    result = provider.generate_with_usage("What is the weather?")

    assert result == ProviderResponse(
        text="Hello, world!",
        usage=Usage(input_tokens=13, output_tokens=7, total_tokens=20),
    )
