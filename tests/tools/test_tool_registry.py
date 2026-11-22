import pytest

from ai_agent.tools.tool_registry import (
    create_registry,
)


def test_registry_contains_tools():
    registry = create_registry()

    assert "get_order_status" in registry.names()
    assert "get_customer" in registry.names()
    assert "search_faq" in registry.names()


def test_registry_retrieves_tool():
    registry = create_registry()

    tool = registry.get("get_order_status")

    assert tool.name == "get_order_status"
    assert callable(tool.handler)


def test_unknown_tool():
    registry = create_registry()

    with pytest.raises(ValueError, match="Unsupported tool"):
        registry.get("unknown")
