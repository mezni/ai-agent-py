from ai_agent_py.application.errors import LlmServiceError


class LlmConfigurationError(LlmServiceError):
    """Raised when LLM configuration is invalid."""


class LlmRequestError(LlmServiceError):
    """Raised when the LLM request fails."""


class LlmResponseError(LlmServiceError):
    """Raised when the provider response is invalid."""
