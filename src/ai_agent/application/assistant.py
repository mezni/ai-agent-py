from ai_agent.application.model_client import ModelClient
from ai_agent.domain.models import ModelRequest, ModelResponse


class CustomerSupportAssistant:
    def __init__(self, model_client: ModelClient):
        self.model_client = model_client

    def answer(self, message: str) -> ModelResponse:

        request = ModelRequest(
            message=message,
            instructions=(
                "You are a professional customer support assistant. "
                "Answer clearly and concisely."
            ),
        )

        return self.model_client.generate(request)


from collections.abc import Iterator


class Assistant:
    def __init__(self, model_client):
        self.model_client = model_client

    def ask(self, prompt: str) -> str:
        return self.model_client.generate(prompt)

    def ask_stream(self, prompt: str) -> Iterator[str]:
        yield from self.model_client.stream(prompt)
