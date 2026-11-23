from ollama import Client


class OllamaProvider:
    def __init__(
        self,
        model: str = "qwen3:4b",
        host: str = "http://localhost:11434",
    ) -> None:
        self.model = model
        self.client = Client(host=host)

    def generate(self, prompt: str) -> str:
        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            stream=False,
        )

        return response.message.content or ""

    def stream(self, prompt: str):
        response_stream = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            stream=True,
        )

        for chunk in response_stream:
            content = chunk.message.content

            if content:
                yield content
