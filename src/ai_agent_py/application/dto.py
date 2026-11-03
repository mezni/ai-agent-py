from dataclasses import dataclass, field
from typing import Any

from ai_agent_py.application.security.actor import AuthenticatedActor
from ai_agent_py.domain.entities import RefundAssessment
from ai_agent_py.domain.enums import AgentIntent, ExecutionStatus


@dataclass(frozen=True)
class ProcessTicketRequest:
    ticket_id: str
    actor: AuthenticatedActor


@dataclass(frozen=True)
class TicketClassification:
    intent: AgentIntent
    category: str
    summary: str
    entities: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AgentResult:
    execution_id: str
    ticket_id: str
    customer_id: str
    classification: TicketClassification
    refund_assessment: RefundAssessment | None
    suggested_response: str
    status: ExecutionStatus
    reasons: tuple[str, ...] = ()
