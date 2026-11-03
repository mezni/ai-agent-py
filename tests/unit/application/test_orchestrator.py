import pytest

from ai_agent_py.application.orchestrator import CustomAgentOrchestrator
from ai_agent_py.domain.entities import Customer, Ticket
from ai_agent_py.domain.enums import TicketStatus
from ai_agent_py.domain.services.refund_policy import RefundPolicyService


class FakeLlmService:
    def __init__(self) -> None:
        self.responses: list[str] = []
        self.requests = []

    def generate(self, request):
        from ai_agent_py.application.interfaces.llm_service import LlmResponse

        self.requests.append(request)
        return LlmResponse(content=self.responses.pop(0), model="fake-model")


class FakeTicketRepository:
    def __init__(self, tickets: list[Ticket]) -> None:
        self._tickets = {ticket.ticket_id: ticket for ticket in tickets}

    def get_by_id(self, ticket_id: str) -> Ticket | None:
        return self._tickets.get(ticket_id)

    def get_by_customer_id(self, customer_id: str) -> list[Ticket]:
        return [ticket for ticket in self._tickets.values() if ticket.customer_id == customer_id]


class FakeCustomerRepository:
    def __init__(self, customers: list[Customer]) -> None:
        self._customers = {customer.customer_id: customer for customer in customers}

    def get_by_id(self, customer_id: str) -> Customer | None:
        return self._customers.get(customer_id)


class FakeOrderRepository:
    def get_by_id(self, order_id: str):
        return None

    def get_by_customer_id(self, customer_id: str) -> list:
        return []


@pytest.fixture
def fake_llm() -> FakeLlmService:
    return FakeLlmService()


@pytest.fixture
def orchestrator(fake_llm: FakeLlmService) -> CustomAgentOrchestrator:
    return CustomAgentOrchestrator(
        ticket_repository=FakeTicketRepository(
            [
                Ticket(
                    ticket_id="ticket-001",
                    customer_id="CUST-001",
                    subject="Order status",
                    description="Where is my order?",
                    status=TicketStatus.OPEN,
                )
            ]
        ),
        customer_repository=FakeCustomerRepository(
            [
                Customer(
                    customer_id="CUST-001",
                    email="customer@example.test",
                )
            ]
        ),
        order_repository=FakeOrderRepository(),
        llm_service=fake_llm,
        refund_policy_service=RefundPolicyService(),
    )


@pytest.mark.unit
def test_process_ticket_raises_when_ticket_missing(orchestrator):
    from ai_agent_py.application.dto import ProcessTicketRequest
    from ai_agent_py.application.errors import TicketNotFoundError

    request = ProcessTicketRequest(
        ticket_id="missing-ticket",
        actor_id="support-agent-1",
    )

    with pytest.raises(TicketNotFoundError):
        orchestrator.process(request)


@pytest.mark.unit
def test_process_ticket_classifies_and_returns_suggestion(
    orchestrator,
    fake_llm,
):
    from ai_agent_py.application.dto import ProcessTicketRequest
    from ai_agent_py.domain.enums import ExecutionStatus

    fake_llm.responses = [
        '{"intent":"ORDER_INQUIRY","category":"order_status",'
        '"summary":"Customer asks about order status",'
        '"entities":{"order_id":"order-001"}}',
        '{"suggested_response":"I can help check your order status."}',
    ]

    result = orchestrator.process(
        ProcessTicketRequest(
            ticket_id="ticket-001",
            actor_id="support-agent-1",
        )
    )

    assert result.ticket_id == "ticket-001"
    assert result.suggested_response
    assert result.status == ExecutionStatus.COMPLETED
    assert result.refund_assessment is None
    assert len(fake_llm.requests) == 2


@pytest.mark.unit
def test_process_ticket_rejects_invalid_intent(
    orchestrator,
    fake_llm,
):
    from ai_agent_py.application.dto import ProcessTicketRequest
    from ai_agent_py.application.errors import InvalidLlmOutputError

    fake_llm.responses = [
        '{"intent":"UNSUPPORTED_INTENT","category":"unknown","summary":"Test", "entities":{}}'
    ]

    with pytest.raises(InvalidLlmOutputError):
        orchestrator.process(
            ProcessTicketRequest(
                ticket_id="ticket-001",
                actor_id="support-agent-1",
            )
        )
