from ai_agent.prompts.ticket_prompts import (
    TICKET_CLASSIFICATION_PROMPT,
)


def build_ticket_classification_prompt(
    ticket: str,
) -> str:

    if not ticket.strip():
        raise ValueError("Ticket cannot be empty.")

    return TICKET_CLASSIFICATION_PROMPT.format(ticket=ticket)
