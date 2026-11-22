import pytest

from ai_agent.tools.tool_dispatcher import (
    ToolDispatcher,
    ToolExecutionError,
)
from ai_agent.tools.tool_registry import (
    create_registry,
)


def test_dispatch_order_tool():
    dispatcher = ToolDispatcher(create_registry())

    result = dispatcher.execute(
        "get_order_status",
        '{"order_id": "4821"}',
    )

    assert result["found"] is True
    assert result["order"]["status"] == "shipped"


def test_dispatch_faq_tool():
    dispatcher = ToolDispatcher(create_registry())

    result = dispatcher.execute(
        "search_faq",
        '{"query": "shipping"}',
    )

    assert "results" in result


def test_dispatch_customer_tool():
    dispatcher = ToolDispatcher(create_registry())

    result = dispatcher.execute(
        "get_customer",
        '{"customer_id": "C100"}',
    )

    assert result["found"] is True


def test_unknown_tool():
    dispatcher = ToolDispatcher(create_registry())

    with pytest.raises(ToolExecutionError):
        dispatcher.execute(
            "unknown",
            "{}",
        )


def test_invalid_arguments():
    dispatcher = ToolDispatcher(create_registry())

    with pytest.raises(ToolExecutionError):
        dispatcher.execute(
            "get_order_status",
            '{"order_id": "4821", "extra": "value"}',
        )
