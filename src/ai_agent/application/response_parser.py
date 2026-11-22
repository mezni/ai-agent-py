from ai_agent.application.errors import (
    LLMIncompleteResponseError,
    LLMParsingError,
    LLMRefusalError,
)
from ai_agent.domain.ticket_classification import (
    TicketClassification,
)


def parse_ticket_classification(response) -> TicketClassification:
    if response.status == "incomplete":
        raise LLMIncompleteResponseError(
            "The model response was incomplete."
        )

    if response.status != "completed":
        raise LLMParsingError(
            f"Unexpected response status: {response.status}"
        )

    for item in response.output:
        if item.type == "message":
            for content in item.content:
                if content.type == "refusal":
                    raise LLMRefusalError(
                        "The model refused the request."
                    )

    result = response.output_parsed

    if result is None:
        raise LLMParsingError(
            "No parsed output was returned."
        )

    if not isinstance(result, TicketClassification):
        raise LLMParsingError(
            "Unexpected parsed output type."
        )

    return result
