import re

from ai_agent.application.memory_extractor import MemoryExtractor
from ai_agent.domain.conversation import Message, MessageRole
from ai_agent.domain.memory import MemoryFact


class TicketMemoryExtractor(MemoryExtractor):
    def extract(
        self,
        messages: list[Message],
    ) -> list[MemoryFact]:

        facts = {}

        for message in messages:
            if message.role != MessageRole.USER:
                continue

            text = message.content.lower()

            order_match = re.search(
                r"\border\s*#?\s*(\d+)\b",
                text,
            )

            if order_match:
                facts["order_id"] = order_match.group(1)

            if "prefer email" in text or "email updates" in text:
                facts["communication_preference"] = "email"

            if "prefer phone" in text or "phone updates" in text:
                facts["communication_preference"] = "phone"

            if "not arrived" in text or "not delivered" in text:
                facts["issue"] = "order_not_delivered"

        return [MemoryFact(key=key, value=value) for key, value in facts.items()]
