from ai_agent.application.memory_retriever import MemoryRetriever
from ai_agent.domain.memory import MemoryFact


def test_retrieve_relevant_memory():
    retriever = MemoryRetriever()

    facts = [
        MemoryFact("order_id", "4821"),
        MemoryFact("communication_preference", "email"),
    ]

    result = retriever.retrieve(
        "What is my order number?",
        facts,
    )

    assert any(fact.key == "order_id" for fact in result)
