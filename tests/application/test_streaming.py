from ai_agent.application.assistant import Assistant


class FakeModelClient:
    def generate(self, prompt: str) -> str:
        return "Complete response"

    def stream(self, prompt: str):
        yield "Your "
        yield "order "
        yield "is "
        yield "being processed."


def test_assistant_streams_chunks():
    assistant = Assistant(
        model_client=FakeModelClient()
    )

    chunks = list(
        assistant.ask_stream("Check order #4821")
    )

    assert chunks == [
        "Your ",
        "order ",
        "is ",
        "being processed.",
    ]


def test_streamed_chunks_can_be_reconstructed():
    assistant = Assistant(
        model_client=FakeModelClient()
    )

    result = "".join(
        assistant.ask_stream("Check order #4821")
    )

    assert result == "Your order is being processed."
