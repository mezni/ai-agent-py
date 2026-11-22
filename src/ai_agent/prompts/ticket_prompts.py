from ai_agent.prompts.prompt_template import PromptTemplate


TICKET_CLASSIFICATION_V1 = PromptTemplate(
    name="ticket_classification",
    version="1.0.0",
    description="Classifies customer support tickets.",
    template="""
You are a customer support ticket classification assistant.

Your task is to classify the customer ticket.

Possible categories:
- order_status
- refund
- technical_support
- account
- general

Rules:
- Identify the primary category.
- Extract the order ID if present.
- Determine whether an order lookup is required.
- Do not invent missing information.

Customer ticket:
{ticket}
""".strip(),
)


TICKET_CLASSIFICATION_V2 = PromptTemplate(
    name="ticket_classification",
    version="2.0.0",
    description="Classifies customer support tickets with examples.",
    template="""
You are a customer support ticket classification assistant.

Classify the ticket into exactly one category:
- order_status
- refund
- technical_support
- account
- general

Examples:

Ticket: My package hasn't arrived.
Category: order_status

Ticket: I want my money back.
Category: refund

Ticket: I can't log into my account.
Category: account

Rules:
- Identify the primary category.
- Extract the order ID if present.
- Determine whether an order lookup is required.
- Do not invent missing information.

Customer ticket:
{ticket}
""".strip(),
)
