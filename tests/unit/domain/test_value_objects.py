from decimal import Decimal

import pytest

from ai_agent_py.domain.value_objects import Money


@pytest.mark.unit
def test_money_accepts_decimal_amount() -> None:
    money = Money(Decimal("89.99"))

    assert money.amount == Decimal("89.99")
    assert money.currency == "CAD"


@pytest.mark.unit
def test_money_normalizes_currency() -> None:
    money = Money(Decimal("10.00"), "cad")

    assert money.currency == "CAD"


@pytest.mark.unit
def test_money_rejects_float() -> None:
    with pytest.raises(TypeError):
        Money(89.99)  # type: ignore[arg-type]


@pytest.mark.unit
def test_money_rejects_invalid_currency() -> None:
    with pytest.raises(ValueError):
        Money(Decimal("10.00"), "CANADA")


@pytest.mark.unit
def test_money_rejects_non_finite_amount() -> None:
    with pytest.raises(ValueError):
        Money(Decimal("NaN"))


@pytest.mark.unit
def test_money_detects_negative_amount() -> None:
    money = Money(Decimal("-10.00"))

    assert money.is_negative()
