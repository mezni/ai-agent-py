import os

from openai import OpenAI

from ai_agent.application.response_parser import (
    parse_ticket_classification,
)
from ai_agent.application.retry import (
    execute_with_retry,
)
from ai_agent.application.ticket_validation import (
    validate_ticket_classification,
)
from ai_agent.domain.ticket_classification import (
    TicketClassification,
)
from ai_agent.prompts.prompt_builder import (
    build_ticket_classification_prompt,
)

client = OpenAI(
    timeout=30.0,
    max_retries=0,
)


def classify_ticket(ticket: str) -> TicketClassification:
    if not ticket.strip():
        raise ValueError("Ticket cannot be empty")

    prompt = build_ticket_classification_prompt(ticket)

    def call_model():
        return client.responses.parse(
            model=os.environ["OPENAI_MODEL"],
            input=prompt,
            text_format=TicketClassification,
        )

    response = execute_with_retry(call_model)

    parsed = parse_ticket_classification(response)

    validated = validate_ticket_classification(parsed)

    return validated
