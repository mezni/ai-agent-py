from dataclasses import dataclass
from enum import StrEnum

from ai_agent_py.application.security.errors import (
    AuthenticationError,
)


class ActorRole(StrEnum):
    SUPPORT_AGENT = "SUPPORT_AGENT"
    SUPERVISOR = "SUPERVISOR"
    ADMIN = "ADMIN"


@dataclass(frozen=True)
class AuthenticatedActor:
    actor_id: str
    role: ActorRole
    customer_scope: frozenset[str] | None = None

    def __post_init__(self) -> None:
        if not self.actor_id.strip():
            raise AuthenticationError("Authenticated actor ID must not be empty.")

        if not isinstance(self.role, ActorRole):
            raise AuthenticationError("Actor role must be a recognized role.")
