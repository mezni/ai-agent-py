import pytest

from ai_agent_py import __version__


@pytest.mark.unit
def test_package_has_version() -> None:
    assert __version__ == "0.1.0"


@pytest.mark.unit
def test_package_version_is_not_empty() -> None:
    assert __version__
