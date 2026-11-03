from ai_agent_py.application.errors import ApplicationError


class GuardrailViolationError(ApplicationError):
    """Raised when an agent request violates a guardrail."""


class UnsafeToolCallError(GuardrailViolationError):
    """Raised when a tool call is invalid or not permitted."""


class UnsafeResponseError(GuardrailViolationError):
    """Raised when a generated response fails validation."""
