import pytest

from ai_agent_py.application.dto import ProcessTicketRequest
from ai_agent_py.application.guardrails.errors import (
    GuardrailViolationError,
)
from ai_agent_py.application.guardrails.input_validation import (
    validate_process_ticket_request,
    validate_ticket_text,
)
from ai_agent_py.application.security.actor import (
    ActorRole,
    AuthenticatedActor,
)


def build_actor(actor_id: str = "agent-001") -> AuthenticatedActor:
    return AuthenticatedActor(
        actor_id=actor_id,
        role=ActorRole.SUPPORT_AGENT,
        customer_scope=frozenset({"customer-001"}),
    )


def test_valid_request_is_accepted():
    validate_process_ticket_request(
        ProcessTicketRequest(
            ticket_id="ticket-001",
            actor=build_actor(),
        )
    )


def test_request_rejects_empty_ticket_id():
    with pytest.raises(GuardrailViolationError):
        validate_process_ticket_request(
            ProcessTicketRequest(
                ticket_id="",
                actor=build_actor(),
            )
        )


def test_ticket_text_rejects_empty_content():
    with pytest.raises(GuardrailViolationError):
        validate_ticket_text("  ")


def test_ticket_text_rejects_oversized_content():
    with pytest.raises(GuardrailViolationError):
        validate_ticket_text("x" * 12_001)


def test_ticket_text_trims_whitespace():
    assert validate_ticket_text("  Help with my order  ") == ("Help with my order")


@pytest.mark.parametrize(
    "ticket_id,actor_id",
    [
        ("x" * 129, "agent-001"),
        ("ticket-001", "x" * 129),
    ],
)
def test_request_rejects_oversized_identifiers(ticket_id, actor_id):
    with pytest.raises(GuardrailViolationError):
        validate_process_ticket_request(
            ProcessTicketRequest(
                ticket_id=ticket_id,
                actor=build_actor(actor_id),
            )
        )


def test_request_rejects_invalid_type():
    with pytest.raises(GuardrailViolationError):
        validate_process_ticket_request("not-a-request")


def test_ticket_text_rejects_non_string():
    with pytest.raises(GuardrailViolationError):
        validate_ticket_text(123)
