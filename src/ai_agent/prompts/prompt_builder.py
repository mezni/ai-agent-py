from ai_agent.prompts.prompt_registry import create_registry


def build_ticket_classification_prompt(ticket: str) -> str:
    if not ticket.strip():
        raise ValueError("Ticket cannot be empty")

    registry = create_registry()

    template = registry.get(
        name="ticket_classification",
        version="1.0.0",
    )

    return template.render(ticket=ticket)
