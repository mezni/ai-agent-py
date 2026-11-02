from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "CAD"

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            raise TypeError("Money amount must be a Decimal.")

        if not self.amount.is_finite():
            raise ValueError("Money amount must be finite.")

        if len(self.currency) != 3 or not self.currency.isalpha():
            raise ValueError("Currency must be a three-letter code.")

        object.__setattr__(self, "currency", self.currency.upper())

    def is_negative(self) -> bool:
        return self.amount < Decimal("0")

    def is_greater_than(self, other: "Money") -> bool:
        self._ensure_same_currency(other)
        return self.amount > other.amount

    def _ensure_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError("Currency mismatch.")
