import json

import pytest

from ai_agent.tools.tool_executor import (
    execute_tool,
)


def test_execute_order_tool():
    result = execute_tool(
        "get_order_status",
        '{"order_id": "4821"}',
    )

    parsed = json.loads(result)

    assert parsed["found"] is True
    assert parsed["order"]["status"] == "shipped"


def test_unsupported_tool():
    with pytest.raises(ValueError, match="Unsupported tool"):
        execute_tool(
            "unknown_tool",
            "{}",
        )


def test_invalid_arguments():
    with pytest.raises(Exception):
        execute_tool(
            "get_order_status",
            '{"order_id": "4821", "extra": "value"}',
        )


def test_missing_order_id():
    with pytest.raises(Exception):
        execute_tool(
            "get_order_status",
            "{}",
        )
