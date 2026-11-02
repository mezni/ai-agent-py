class DomainError(Exception):
    """Base exception for domain-related errors."""


class InvalidDomainState(DomainError):
    """Raised when a domain object enters an invalid state."""


class PolicyEvaluationError(DomainError):
    """Raised when a policy cannot be evaluated safely."""
