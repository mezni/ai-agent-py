from ai_agent_py.application.tools.context import ToolExecutionContext
from ai_agent_py.application.tools.contracts import (
    ToolCall,
    ToolStatus,
)
from ai_agent_py.application.tools.registry import ToolRegistry


class FakeTool:
    def __init__(self, name):
        self.name = name

    def execute(self, call, context):
        from ai_agent_py.application.tools.contracts import ToolResult

        return ToolResult(
            tool_name=self.name,
            status=ToolStatus.SUCCESS,
            data={"ok": True},
        )


def test_registry_rejects_unknown_tool():
    registry = ToolRegistry([FakeTool("customer_lookup")])
    context = ToolExecutionContext(
        actor_id="agent-1",
        actor_role="SUPPORT_AGENT",
        customer_id="customer-1",
        ticket_id="ticket-1",
    )

    result = registry.execute(
        ToolCall(name="unknown_tool", arguments={}),
        context,
    )

    assert result.status == ToolStatus.INVALID_ARGUMENTS


def test_registry_executes_registered_tool():
    registry = ToolRegistry([FakeTool("customer_lookup")])
    context = ToolExecutionContext(
        actor_id="agent-1",
        actor_role="SUPPORT_AGENT",
        customer_id="customer-1",
        ticket_id="ticket-1",
    )

    result = registry.execute(
        ToolCall(
            name="customer_lookup",
            arguments={"customer_id": "customer-1"},
        ),
        context,
    )

    assert result.status == ToolStatus.SUCCESS
    assert result.data == {"ok": True}


def test_registry_rejects_duplicate_tool_names():
    import pytest

    with pytest.raises(ValueError):
        ToolRegistry(
            [
                FakeTool("customer_lookup"),
                FakeTool("customer_lookup"),
            ]
        )
