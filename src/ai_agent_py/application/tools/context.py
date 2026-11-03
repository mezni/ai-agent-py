from dataclasses import dataclass

from ai_agent_py.application.security.actor import AuthenticatedActor


@dataclass(frozen=True)
class ToolExecutionContext:
    actor: AuthenticatedActor
    customer_id: str
    ticket_id: str
