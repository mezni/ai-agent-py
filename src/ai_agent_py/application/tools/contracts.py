from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class ToolStatus(StrEnum):
    SUCCESS = "SUCCESS"
    DENIED = "DENIED"
    INVALID_ARGUMENTS = "INVALID_ARGUMENTS"
    NOT_FOUND = "NOT_FOUND"
    FAILED = "FAILED"


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class ToolResult:
    tool_name: str
    status: ToolStatus
    data: dict[str, Any] | None = None
    reason: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.status == ToolStatus.SUCCESS
