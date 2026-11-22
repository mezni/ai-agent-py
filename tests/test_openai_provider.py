from unittest.mock import Mock

from ai_agent.providers.openai_provider import OpenAIProvider
from ai_agent.domain.models import ModelRequest


def test_openai_provider_normalizes_response():

    mock_client = Mock()

    mock_client.responses.create.return_value = Mock(
        output_text="Your order is being processed.",
        model="test-model",
        usage=Mock(
            input_tokens=10,
            output_tokens=8,
        ),
    )

    provider = OpenAIProvider(client=mock_client)

    response = provider.generate(
        ModelRequest(
            message="Where is my order?",
            model="test-model",
        )
    )

    assert response.text == "Your order is being processed."
    assert response.input_tokens == 10
    assert response.output_tokens == 8
    assert response.total_tokens == 18

    mock_client.responses.create.assert_called_once()
