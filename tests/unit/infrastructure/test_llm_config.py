import pytest

from ai_agent_py.infrastructure.llm.config import LlmConfig


@pytest.mark.unit
def test_config_loads_from_environment(monkeypatch):
    monkeypatch.setenv("LLM_BASE_URL", "https://llm.example.test/v1/")
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setenv("LLM_MODEL", "test-model")
    monkeypatch.setenv("LLM_TIMEOUT_SECONDS", "12.5")

    config = LlmConfig.from_environment()

    assert config.base_url == "https://llm.example.test/v1"
    assert config.api_key == "test-key"
    assert config.model == "test-model"
    assert config.timeout_seconds == 12.5


@pytest.mark.unit
def test_config_requires_api_key(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.setenv("LLM_MODEL", "test-model")

    with pytest.raises(ValueError):
        LlmConfig.from_environment()


@pytest.mark.unit
def test_config_requires_model(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.delenv("LLM_MODEL", raising=False)

    with pytest.raises(ValueError):
        LlmConfig.from_environment()


@pytest.mark.unit
def test_config_requires_positive_timeout(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setenv("LLM_MODEL", "test-model")
    monkeypatch.setenv("LLM_TIMEOUT_SECONDS", "0")

    with pytest.raises(ValueError):
        LlmConfig.from_environment()
