from dataclasses import asdict

from ai_agent.application.generation_config import (
    GenerationConfig,
)


def build_generation_options(
    config: GenerationConfig,
) -> dict:
    options = asdict(config)

    return {
        key: value
        for key, value in options.items()
        if value is not None
    }
