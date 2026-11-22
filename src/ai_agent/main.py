from ai_agent.application.assistant import CustomerSupportAssistant
from ai_agent.providers.openai_provider import OpenAIProvider


def main():

    model_client = OpenAIProvider()

    assistant = CustomerSupportAssistant(model_client=model_client)

    response = assistant.answer("My order #4821 has not arrived.")

    print(response.text)

    print(f"Input tokens: {response.input_tokens}")
    print(f"Output tokens: {response.output_tokens}")


if __name__ == "__main__":
    main()
