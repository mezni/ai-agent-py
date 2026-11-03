class ApplicationError(Exception):
    """Base class for expected application failures."""


class TicketNotFoundError(ApplicationError):
    """Raised when the requested ticket does not exist."""


class CustomerNotFoundError(ApplicationError):
    """Raised when a ticket's customer record is missing."""


class LlmServiceError(ApplicationError):
    """Raised when the LLM service cannot complete a request."""


class InvalidLlmOutputError(ApplicationError):
    """Raised when LLM output fails application-level validation."""
