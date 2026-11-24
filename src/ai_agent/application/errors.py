class LLMError(Exception):
    """Base exception for LLM application errors."""


class LLMTransientError(LLMError):
    """An error that may succeed on a later attempt."""


class LLMRateLimitError(LLMTransientError):
    """Provider rate limit was reached."""

    def __init__(
        self,
        message: str,
        retry_after: float | None = None,
    ):
        super().__init__(message)
        self.retry_after = retry_after


class LLMTimeoutError(LLMTransientError):
    """The model request timed out."""


class LLMConnectionError(LLMTransientError):
    """The provider could not be reached."""


class LLMPermanentError(LLMError):
    """Retrying the same request will not resolve the error."""


class LLMAuthenticationError(LLMPermanentError):
    """Authentication failed."""


class LLMInvalidRequestError(LLMPermanentError):
    """The request was invalid."""


class LLMResponseError(LLMError):
    """The response could not be interpreted."""
