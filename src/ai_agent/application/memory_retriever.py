from ai_agent.domain.memory import MemoryFact


class MemoryRetriever:
    def retrieve(
        self,
        query: str,
        facts: list[MemoryFact],
    ) -> list[MemoryFact]:

        query_words = set(query.lower().split())

        relevant = []

        for fact in facts:
            searchable = (fact.key + " " + fact.value).lower()

            if any(word in searchable for word in query_words if len(word) > 2):
                relevant.append(fact)

        return relevant
