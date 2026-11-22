import os
from dotenv import load_dotenv
from openai import OpenAI

from ai_agent.domain.ticket_classification import (
    TicketClassification,
)

load_dotenv()

client = OpenAI(
    timeout=30.0,
    max_retries=2,
)


def classify_ticket(ticket: str) -> TicketClassification:
    if not ticket.strip():
        raise ValueError("Ticket cannot be empty")

    response = client.responses.parse(
        model=os.getenv("OPENAI_MODEL"),
        input=[
            {
                "role": "system",
                "content": """
You are a customer support ticket classifier.

Classify the ticket using the provided schema.

Rules:
- Identify the primary category.
- Extract the order ID if present.
- An order lookup is needed only when the ticket
  requires checking order information.
- Do not invent an order ID.
- Use null when no order ID is available.
""".strip(),
            },
            {
                "role": "user",
                "content": ticket,
            },
        ],
        text_format=TicketClassification,
    )

    result = response.output_parsed

    if result is None:
        raise RuntimeError("Model did not return a parsed classification")

    return result


if __name__ == "__main__":
    result = classify_ticket("My order #4821 has not arrived.")

    print(result.model_dump_json(indent=2))
