import json
from typing import Any

from pydantic import ValidationError

from ai_agent.tools.tool_registry import ToolRegistry


class ToolExecutionError(Exception):
    """Tool execution failed."""


class ToolDispatcher:
    def __init__(self, registry: ToolRegistry) -> None:
        self._registry = registry

    def execute(
        self,
        tool_name: str,
        arguments: str,
    ) -> Any:
        try:
            definition = self._registry.get(tool_name)

            parsed_arguments = json.loads(arguments)

            validated_arguments = definition.arguments_model.model_validate(
                parsed_arguments
            )

            result = definition.handler(**validated_arguments.model_dump())

            return result

        except (ValueError, ValidationError) as exc:
            raise ToolExecutionError("Invalid tool request.") from exc

        except Exception as exc:
            raise ToolExecutionError("Tool execution failed.") from exc
