class LlmError(Exception):
    """Base exception for LLM integration failures."""


class LlmConfigurationError(LlmError):
    """Raised when provider configuration is invalid."""


class LlmProviderError(LlmError):
    """Raised when the provider request fails."""


class LlmResponseError(LlmError):
    """Raised when the provider response is invalid."""
