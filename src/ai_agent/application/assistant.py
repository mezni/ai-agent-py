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
