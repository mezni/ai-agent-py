from abc import ABC, abstractmethod

from ai_agent.domain.conversation import Message


class MemorySummarizer(ABC):
    @abstractmethod
    def summarize(
        self,
        previous_summary: str,
        messages: list[Message],
    ) -> str:
        pass
