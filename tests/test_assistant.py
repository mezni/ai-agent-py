from ai_agent.application.assistant import CustomerSupportAssistant
from ai_agent.domain.models import ModelResponse


class FakeModelClient:
    def generate(self, request):
        return ModelResponse(
            text="Your order is being processed.",
            model="fake-model",
            input_tokens=10,
            output_tokens=8,
            total_tokens=18,
        )


def test_assistant_returns_response():

    assistant = CustomerSupportAssistant(model_client=FakeModelClient())

    response = assistant.answer("Where is my order?")

    assert response.text == "Your order is being processed."
    assert response.model == "fake-model"
    assert response.total_tokens == 18
