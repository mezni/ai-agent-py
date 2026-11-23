from ai_agent.application.conversation_store import ConversationStore
from ai_agent.application.memory_extractor import MemoryExtractor
from ai_agent.application.memory_retriever import MemoryRetriever
from ai_agent.application.memory_summarizer import MemorySummarizer
from ai_agent.domain.conversation import Message


class MemoryManager:
    def __init__(
        self,
        store: ConversationStore,
        summarizer: MemorySummarizer,
        extractor: MemoryExtractor,
        retriever: MemoryRetriever,
    ):
        self.store = store
        self.summarizer = summarizer
        self.extractor = extractor
        self.retriever = retriever

    def process_conversation(
        self,
        owner_id: str,
        previous_summary: str,
        messages: list[Message],
    ) -> str:

        summary = self.summarizer.summarize(
            previous_summary,
            messages,
        )

        facts = self.extractor.extract(messages)

        for fact in facts:
            self.store.save_fact(owner_id, fact)

        return summary

    def retrieve_relevant_memory(
        self,
        owner_id: str,
        query: str,
    ):

        facts = self.store.get_facts(owner_id)

        return self.retriever.retrieve(query, facts)
