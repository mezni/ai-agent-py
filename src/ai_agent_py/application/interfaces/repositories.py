from typing import Protocol

from ai_agent_py.domain.entities import Customer, Order, Ticket


class CustomerRepository(Protocol):
    def get_by_id(self, customer_id: str) -> Customer | None:
        """Return a customer by ID, or None if not found."""


class OrderRepository(Protocol):
    def get_by_id(self, order_id: str) -> Order | None:
        """Return an order by ID, or None if not found."""

    def get_by_customer_id(self, customer_id: str) -> list[Order]:
        """Return orders belonging to the specified customer."""


class TicketRepository(Protocol):
    def get_by_id(self, ticket_id: str) -> Ticket | None:
        """Return a ticket by ID, or None if not found."""

    def get_by_customer_id(self, customer_id: str) -> list[Ticket]:
        """Return tickets belonging to the specified customer."""
