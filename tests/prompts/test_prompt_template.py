import pytest

from ai_agent.prompts.prompt_template import PromptTemplate


def test_render_template():
    template = PromptTemplate(
        name="test",
        version="1.0.0",
        description="Test prompt",
        template="Hello {name}",
    )

    result = template.render(name="Alice")

    assert result == "Hello Alice"


def test_render_missing_variable():
    template = PromptTemplate(
        name="test",
        version="1.0.0",
        description="Test prompt",
        template="Hello {name}",
    )

    with pytest.raises(ValueError, match="Missing prompt variable"):
        template.render()


def test_template_metadata():
    template = PromptTemplate(
        name="test",
        version="1.0.0",
        description="Test prompt",
        template="Hello {name}",
    )

    assert template.name == "test"
    assert template.version == "1.0.0"
