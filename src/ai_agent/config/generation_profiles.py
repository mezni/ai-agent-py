from ai_agent.application.generation_config import (
    GenerationConfig,
)


TICKET_CLASSIFICATION = GenerationConfig(
    temperature=0.0,
    max_output_tokens=300,
)

ENTITY_EXTRACTION = GenerationConfig(
    temperature=0.0,
    max_output_tokens=200,
)

CUSTOMER_RESPONSE = GenerationConfig(
    temperature=0.4,
    max_output_tokens=700,
)

RAG_RESPONSE = GenerationConfig(
    temperature=0.2,
    max_output_tokens=800,
)
