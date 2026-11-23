from abc import ABC, abstractmethod

from ai_agent.domain.conversation import Message
from ai_agent.domain.memory import MemoryFact


class MemoryExtractor(ABC):
    @abstractmethod
    def extract(
        self,
        messages: list[Message],
    ) -> list[MemoryFact]:
        pass
