from ai_agent.application.conversation_store import ConversationStore
from ai_agent.application.memory_manager import MemoryManager
from ai_agent.application.memory_retriever import MemoryRetriever
from ai_agent.domain.memory import MemoryFact


class FakeSummarizer:
    def summarize(self, previous_summary, messages):
        return "Customer is investigating order #4821."


class FakeExtractor:
    def extract(self, messages):
        return [
            MemoryFact("order_id", "4821"),
        ]


def test_memory_manager_processes_conversation(tmp_path):
    store = ConversationStore(str(tmp_path / "test.db"))

    manager = MemoryManager(
        store=store,
        summarizer=FakeSummarizer(),
        extractor=FakeExtractor(),
        retriever=MemoryRetriever(),
    )

    summary = manager.process_conversation(
        owner_id="customer-123",
        previous_summary="",
        messages=[],
    )

    assert "4821" in summary

    facts = manager.retrieve_relevant_memory(
        owner_id="customer-123",
        query="What is my order number?",
    )

    assert facts[0].value == "4821"
