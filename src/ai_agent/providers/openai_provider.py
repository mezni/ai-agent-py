from dataclasses import dataclass

import openai
from openai import OpenAI

from ai_agent.config import settings


@dataclass(frozen=True)
class Usage:
    input_tokens: int
    output_tokens: int
    total_tokens: int


@dataclass(frozen=True)
class ProviderResponse:
    text: str
    usage: Usage


class OpenAIProvider:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            timeout=30.0,
            max_retries=2,
        )

    def generate(self, message: str) -> str:
        return self._create_response(message).output_text

    def generate_with_usage(self, message: str) -> ProviderResponse:
        response = self._create_response(message)
        return ProviderResponse(
            text=response.output_text,
            usage=self.extract_usage(response),
        )

    @staticmethod
    def extract_usage(response: object) -> Usage:
        usage = response.usage
        return Usage(
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            total_tokens=usage.total_tokens,
        )

    def _create_response(self, message: str):
        try:
            return self.client.responses.create(
                model=settings.openai_model,
                instructions="You are a helpful assistant.",
                input=message,
            )

        except openai.AuthenticationError as exc:
            raise RuntimeError("Provider authentication failed") from exc

        except openai.APIConnectionError as exc:
            raise RuntimeError("Provider connection failed") from exc

        except openai.APIStatusError as exc:
            raise RuntimeError(
                f"Provider returned HTTP {exc.status_code}"
            ) from exc
