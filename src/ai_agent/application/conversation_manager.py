from ai_agent.application.conversation_store import ConversationStore
from ai_agent.application.context_manager import ContextManager
from ai_agent.domain.conversation import (
    Conversation,
    ConversationMemory,
    Message,
    MessageRole,
)


class ConversationManager:
    def __init__(
        self,
        store: ConversationStore,
        context_manager: ContextManager,
    ):
        self.store = store
        self.context_manager = context_manager

    def start_conversation(self) -> str:
        conversation = Conversation()

        self.store.create_conversation(conversation)

        return conversation.id

    def add_user_message(
        self,
        conversation_id: str,
        content: str,
    ):
        message = Message(
            role=MessageRole.USER,
            content=content,
        )

        self.store.add_message(conversation_id, message)

    def add_assistant_message(
        self,
        conversation_id: str,
        content: str,
    ):
        message = Message(
            role=MessageRole.ASSISTANT,
            content=content,
        )

        self.store.add_message(conversation_id, message)

    def get_history(
        self,
        conversation_id: str,
    ) -> list[Message]:

        return self.store.get_messages(conversation_id)

    def update_memory(
        self,
        conversation_id: str,
        summary: str,
        facts: list[str],
    ):
        memory = ConversationMemory(
            summary=summary,
            facts=facts,
        )

        self.store.save_memory(conversation_id, memory)

    def build_context(
        self,
        conversation_id: str,
        system_prompt: str,
        current_message: str,
    ) -> list[dict]:

        history = self.get_history(conversation_id)
        memory = self.store.get_memory(conversation_id)

        return self.context_manager.build_context(
            system_prompt=system_prompt,
            history=history,
            current_message=current_message,
            memory=memory,
        )
