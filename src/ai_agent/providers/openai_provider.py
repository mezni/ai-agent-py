import openai
from openai import OpenAI

from ai_agent.config import settings
from ai_agent.domain.models import ModelRequest, ModelResponse


class OpenAIProvider:
    def __init__(self, client: OpenAI | None = None):
        self.client = client or OpenAI(
            api_key=settings.openai_api_key,
            timeout=30.0,
            max_retries=2,
        )

    def generate(self, request: ModelRequest) -> ModelResponse:

        try:
            response = self.client.responses.create(
                model=request.model or settings.openai_model,
                instructions=request.instructions,
                input=request.message,
                max_output_tokens=request.max_output_tokens,
            )

        except openai.AuthenticationError as exc:
            raise RuntimeError("Provider authentication failed") from exc

        except openai.APIConnectionError as exc:
            raise RuntimeError("Provider connection failed") from exc

        except openai.APIStatusError as exc:
            raise RuntimeError(f"Provider returned HTTP {exc.status_code}") from exc

        usage = response.usage

        input_tokens = usage.input_tokens if usage else 0
        output_tokens = usage.output_tokens if usage else 0

        return ModelResponse(
            text=response.output_text,
            model=response.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
        )
