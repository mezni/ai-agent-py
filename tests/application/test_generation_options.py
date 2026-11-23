from ai_agent.application.generation_config import (
    GenerationConfig,
)
from ai_agent.application.generation_options import (
    build_generation_options,
)


def test_generation_options_exclude_none():
    config = GenerationConfig(
        temperature=0.0,
        max_output_tokens=300,
    )

    result = build_generation_options(config)

    assert result == {
        "temperature": 0.0,
        "max_output_tokens": 300,
    }


def test_generation_options_preserve_zero():
    config = GenerationConfig(
        temperature=0.0,
        frequency_penalty=0.0,
    )

    result = build_generation_options(config)

    assert result["temperature"] == 0.0
    assert result["frequency_penalty"] == 0.0


def test_generation_options_support_custom_values():
    config = GenerationConfig(
        temperature=0.7,
        top_p=0.9,
        max_output_tokens=1000,
    )

    result = build_generation_options(config)

    assert result["temperature"] == 0.7
    assert result["top_p"] == 0.9
    assert result["max_output_tokens"] == 1000
