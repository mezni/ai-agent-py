import json
from datetime import date
from pathlib import Path
from typing import Any

from ai_agent_py.domain.entities import Customer, Order, Ticket
from ai_agent_py.domain.enums import OrderStatus, TicketStatus
from ai_agent_py.domain.value_objects import Money


class FixtureDataError(Exception):
    """Raised when a fixture file cannot be read or mapped."""


class JsonFixtureReader:
    def __init__(self, fixture_path: Path) -> None:
        self.fixture_path = fixture_path

    def read_records(self) -> list[dict[str, Any]]:
        try:
            raw_data = json.loads(self.fixture_path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise FixtureDataError(f"Fixture file not found: {self.fixture_path}") from exc
        except json.JSONDecodeError as exc:
            raise FixtureDataError(
                f"Fixture file contains invalid JSON: {self.fixture_path}"
            ) from exc

        if not isinstance(raw_data, list):
            raise FixtureDataError(f"Expected a JSON array in fixture: {self.fixture_path}")

        if not all(isinstance(record, dict) for record in raw_data):
            raise FixtureDataError(
                f"Every fixture record must be a JSON object: {self.fixture_path}"
            )

        return raw_data


class JsonCustomerRepository:
    def __init__(self, fixture_path: Path) -> None:
        self._reader = JsonFixtureReader(fixture_path)

    def get_by_id(self, customer_id: str) -> Customer | None:
        for record in self._reader.read_records():
            if record.get("customer_id") == customer_id:
                try:
                    return Customer(
                        customer_id=record["customer_id"],
                        email=record["email"],
                    )
                except (KeyError, TypeError) as exc:
                    raise FixtureDataError(
                        "Customer fixture record is missing required fields."
                    ) from exc

        return None


class JsonOrderRepository:
    def __init__(self, fixture_path: Path) -> None:
        self._reader = JsonFixtureReader(fixture_path)

    def get_by_id(self, order_id: str) -> Order | None:
        for record in self._reader.read_records():
            if record.get("order_id") == order_id:
                return self._to_entity(record)

        return None

    def get_by_customer_id(self, customer_id: str) -> list[Order]:
        return [
            self._to_entity(record)
            for record in self._reader.read_records()
            if record.get("customer_id") == customer_id
        ]

    @staticmethod
    def _to_entity(record: dict[str, Any]) -> Order:
        try:
            return Order(
                order_id=record["order_id"],
                customer_id=record["customer_id"],
                order_date=date.fromisoformat(record["order_date"]),
                status=OrderStatus(record["status"]),
                total_amount=Money.from_json_value(
                    record["total_amount"],
                    record.get("currency", "CAD"),
                ),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise FixtureDataError(
                "Order fixture record contains invalid or missing fields."
            ) from exc


class JsonTicketRepository:
    def __init__(self, fixture_path: Path) -> None:
        self._reader = JsonFixtureReader(fixture_path)

    def get_by_id(self, ticket_id: str) -> Ticket | None:
        for record in self._reader.read_records():
            if record.get("ticket_id") == ticket_id:
                return self._to_entity(record)

        return None

    def get_by_customer_id(self, customer_id: str) -> list[Ticket]:
        return [
            self._to_entity(record)
            for record in self._reader.read_records()
            if record.get("customer_id") == customer_id
        ]

    @staticmethod
    def _to_entity(record: dict[str, Any]) -> Ticket:
        try:
            return Ticket(
                ticket_id=record["ticket_id"],
                customer_id=record["customer_id"],
                subject=record["subject"],
                description=record["description"],
                status=TicketStatus(record["status"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise FixtureDataError(
                "Ticket fixture record contains invalid or missing fields."
            ) from exc
