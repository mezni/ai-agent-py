import pytest

from ai_agent_py.application.errors import InvalidLlmOutputError
from ai_agent_py.application.structured_output import (
    parse_json_object,
    require_string,
)


def test_parse_json_object_accepts_object():
    assert parse_json_object('{"intent": "ORDER_INQUIRY"}') == {"intent": "ORDER_INQUIRY"}


def test_parse_json_object_rejects_invalid_json():
    with pytest.raises(InvalidLlmOutputError):
        parse_json_object("not-json")


def test_parse_json_object_rejects_array():
    with pytest.raises(InvalidLlmOutputError):
        parse_json_object('["not", "an", "object"]')


def test_require_string_rejects_missing_field():
    with pytest.raises(InvalidLlmOutputError):
        require_string({}, "summary")


def test_require_string_rejects_empty_string():
    with pytest.raises(InvalidLlmOutputError):
        require_string({"summary": "  "}, "summary")


def test_require_string_accepts_valid_string():
    assert (
        require_string(
            {"summary": "  Order status question  "},
            "summary",
        )
        == "Order status question"
    )
