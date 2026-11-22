class LLMApplicationError(Exception):
    """Base error for LLM application failures."""


class LLMRefusalError(LLMApplicationError):
    """The model refused to fulfill the request."""


class LLMIncompleteResponseError(LLMApplicationError):
    """The model response was incomplete."""


class LLMParsingError(LLMApplicationError):
    """The response could not be parsed."""


class LLMValidationError(LLMApplicationError):
    """The response failed validation."""


class LLMRetryExhaustedError(LLMApplicationError):
    """Retry attempts were exhausted."""


class LLMNonRetryableError(LLMApplicationError):
    """The failure should not be retried."""
