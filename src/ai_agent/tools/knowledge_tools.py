FAQS = [
    {
        "question": "How long does shipping take?",
        "answer": "Standard shipping takes 3 to 5 business days.",
    },
    {
        "question": "How can I request a refund?",
        "answer": "Refund requests can be submitted within 30 days.",
    },
    {
        "question": "How do I reset my password?",
        "answer": "Use the password reset option on the login page.",
    },
]


def search_faq(query: str) -> dict:
    query_words = set(query.lower().split())

    matches = []

    for faq in FAQS:
        searchable_text = (faq["question"] + " " + faq["answer"]).lower()

        score = sum(word in searchable_text for word in query_words)

        if score > 0:
            matches.append(
                {
                    "score": score,
                    "question": faq["question"],
                    "answer": faq["answer"],
                }
            )

    matches.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return {
        "results": matches[:3],
    }
