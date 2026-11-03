from ai_agent_py.application.dto import ProcessTicketRequest
from ai_agent_py.application.guardrails.errors import (
    GuardrailViolationError,
)
from ai_agent_py.application.security.actor import AuthenticatedActor


def validate_process_ticket_request(
    request: ProcessTicketRequest,
) -> None:
    if not isinstance(request, ProcessTicketRequest):
        raise GuardrailViolationError("Request has an invalid type.")

    if not isinstance(request.actor, AuthenticatedActor):
        raise GuardrailViolationError("actor must be an authenticated actor.")

    if not request.ticket_id.strip():
        raise GuardrailViolationError("ticket_id must not be empty.")

    if len(request.ticket_id) > 128:
        raise GuardrailViolationError("ticket_id exceeds the maximum length.")

    if len(request.actor.actor_id) > 128:
        raise GuardrailViolationError("actor_id exceeds the maximum length.")


def validate_ticket_text(ticket_text: str) -> str:
    if not isinstance(ticket_text, str):
        raise GuardrailViolationError("Ticket text must be a string.")

    normalized = ticket_text.strip()

    if not normalized:
        raise GuardrailViolationError("Ticket text must not be empty.")

    if len(normalized) > 12_000:
        raise GuardrailViolationError("Ticket text exceeds the allowed length.")

    return normalized
