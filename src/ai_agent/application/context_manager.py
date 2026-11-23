from math import ceil

from ai_agent.domain.conversation import (
    ConversationMemory,
    Message,
    MessageRole,
)


class ContextWindowExceeded(Exception):
    pass


class ContextManager:
    def __init__(
        self,
        max_context_tokens: int = 32000,
        response_reserve_tokens: int = 4000,
    ):
        if max_context_tokens <= 0:
            raise ValueError("Context limit must be positive.")

        if not 0 <= response_reserve_tokens < max_context_tokens:
            raise ValueError("Invalid response token reserve.")

        self.max_context_tokens = max_context_tokens
        self.response_reserve_tokens = response_reserve_tokens

    def estimate_tokens(self, text: str) -> int:
        return ceil(len(text) / 4)

    def estimate_message_tokens(self, message: Message) -> int:
        return self.estimate_tokens(message.content) + 4

    def build_context(
        self,
        system_prompt: str,
        history: list[Message],
        current_message: str,
        memory: ConversationMemory | None = None,
    ) -> list[dict]:

        messages = [
            {
                "role": MessageRole.SYSTEM.value,
                "content": system_prompt,
            }
        ]

        if memory:
            memory_content = "\n".join(
                [
                    f"Conversation summary: {memory.summary}",
                    "Important facts:",
                    *[f"- {fact}" for fact in memory.facts],
                ]
            )

            if memory.summary or memory.facts:
                messages.append(
                    {
                        "role": MessageRole.SYSTEM.value,
                        "content": ("Relevant conversation memory:\n" + memory_content),
                    }
                )

        current = Message(
            role=MessageRole.USER,
            content=current_message,
        )

        fixed_tokens = sum(
            self.estimate_message_tokens(
                Message(
                    role=MessageRole(message["role"]),
                    content=message["content"],
                )
            )
            for message in messages
        )

        fixed_tokens += self.estimate_message_tokens(current)

        budget = self.max_context_tokens - self.response_reserve_tokens

        if fixed_tokens > budget:
            raise ContextWindowExceeded(
                "System prompt, memory and current message "
                "exceed the available context budget."
            )

        selected_history = []
        remaining = budget - fixed_tokens

        # Keep the newest messages first.
        for message in reversed(history):
            cost = self.estimate_message_tokens(message)

            if cost > remaining:
                break

            selected_history.append(message)
            remaining -= cost

        selected_history.reverse()

        messages.extend(
            [
                {
                    "role": message.role.value,
                    "content": message.content,
                }
                for message in selected_history
            ]
        )

        messages.append(
            {
                "role": MessageRole.USER.value,
                "content": current_message,
            }
        )

        return messages
