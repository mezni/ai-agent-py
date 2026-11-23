from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(frozen=True)
class MemoryFact:
    key: str
    value: str
    id: str = field(default_factory=lambda: str(uuid4()))
    confidence: float = 1.0
    source: str = "conversation"
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def __post_init__(self):
        if not self.key.strip():
            raise ValueError("Memory key cannot be empty.")

        if not self.value.strip():
            raise ValueError("Memory value cannot be empty.")

        if not 0 <= self.confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1.")


@dataclass
class LongTermMemory:
    owner_id: str
    summary: str = ""
    facts: list[MemoryFact] = field(default_factory=list)
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
