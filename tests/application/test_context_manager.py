import pytest

from ai_agent.application.context_manager import (
    ContextManager,
    ContextWindowExceeded,
)
from ai_agent.domain.conversation import Message, MessageRole


def test_context_includes_recent_history():
    manager = ContextManager(
        max_context_tokens=1000,
        response_reserve_tokens=100,
    )

    history = [
        Message(MessageRole.USER, "My order is delayed."),
        Message(MessageRole.ASSISTANT, "What is your order ID?"),
    ]

    result = manager.build_context(
        system_prompt="You are a support assistant.",
        history=history,
        current_message="It is #4821.",
    )

    assert len(result) == 4
    assert result[-1]["content"] == "It is #4821."


def test_context_rejects_oversized_message():
    manager = ContextManager(
        max_context_tokens=100,
        response_reserve_tokens=20,
    )

    with pytest.raises(ContextWindowExceeded):
        manager.build_context(
            system_prompt="You are a support assistant.",
            history=[],
            current_message="A" * 1000,
        )


def test_old_history_is_removed_first():
    manager = ContextManager(
        max_context_tokens=100,
        response_reserve_tokens=10,
    )

    history = [
        Message(MessageRole.USER, "OLD " * 100),
        Message(MessageRole.ASSISTANT, "RECENT"),
    ]

    result = manager.build_context(
        system_prompt="Support assistant.",
        history=history,
        current_message="Continue.",
    )

    contents = [message["content"] for message in result]

    assert "RECENT" in contents
    assert "OLD " * 100 not in contents
