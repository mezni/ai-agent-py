import os

from dotenv import load_dotenv
from openai import OpenAI


class CustomerSupportAssistant:
    def __init__(self, client: OpenAI, model: str | None = None):
        self.client = client
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    def answer(self, message: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=(
                "You are a helpful customer support assistant. "
                "Provide clear and concise answers."
            ),
            input=message,
        )

        return response.output_text


def main():
    load_dotenv()

    client = OpenAI()

    assistant = CustomerSupportAssistant(client)

    response = assistant.answer("My order #4821 has not arrived. Can you help?")

    print(response)


if __name__ == "__main__":
    main()
