from ai_agent.providers.openai_provider import OpenAIProvider

provider = OpenAIProvider()

response = provider.generate("My order #4821 has not arrived.")
print (response)