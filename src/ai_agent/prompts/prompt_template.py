from dataclasses import dataclass


@dataclass(frozen=True)
class PromptTemplate:
    name: str
    version: str
    description: str
    template: str

    def render(self, **variables: str) -> str:
        try:
            return self.template.format(**variables)
        except KeyError as exc:
            raise ValueError(f"Missing prompt variable: {exc.args[0]}") from exc
