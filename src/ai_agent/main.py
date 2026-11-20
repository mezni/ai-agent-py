from openai import OpenAI


class CustomerSupportAssistant:

    def __init__(self, client: OpenAI):
        self.client = client

    def answer(self, message: str) -> str:
        response = self.client.responses.create(
            model="YOUR_MODEL",
            instructions=(
                "You are a helpful customer support assistant. "
                "Provide clear and concise answers."
            ),
            input=message,
        )

        return response.output_text


def main():
    client = OpenAI()

    assistant = CustomerSupportAssistant(client)

    response = assistant.answer(
        "My order #4821 has not arrived. Can you help?"
    )

    print(response)


if __name__ == "__main__":
    main()
