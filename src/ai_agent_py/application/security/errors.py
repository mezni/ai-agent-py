from ai_agent_py.application.errors import ApplicationError


class AuthenticationError(ApplicationError):
    """Raised when the actor context is missing or invalid."""


class AuthorizationError(ApplicationError):
    """Raised when the actor lacks the required permission."""


class CustomerScopeError(AuthorizationError):
    """Raised when a request crosses the authorized customer scope."""
