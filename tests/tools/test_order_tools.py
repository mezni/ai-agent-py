from ai_agent.tools.order_tools import (
    get_order_status,
)


def test_order_exists():
    result = get_order_status("4821")

    assert result["found"] is True
    assert result["order"]["status"] == "shipped"


def test_order_not_found():
    result = get_order_status("9999")

    assert result["found"] is False
    assert result["order_id"] == "9999"
