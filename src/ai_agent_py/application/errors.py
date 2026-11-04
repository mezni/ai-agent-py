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


class ApprovalNotFoundError(ApplicationError):
    """Raised when an approval request does not exist."""


class ApprovalAlreadyDecidedError(ApplicationError):
    """Raised when an approval is no longer pending."""


class ApprovalExpiredError(ApplicationError):
    """Raised when an approval request has expired."""


class InvalidApprovalRequestError(ApplicationError):
    """Raised when approval request data is invalid."""
