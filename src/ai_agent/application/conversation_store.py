import json
import sqlite3

from ai_agent.domain.conversation import (
    Conversation,
    ConversationMemory,
    Message,
    MessageRole,
)
from ai_agent.domain.memory import MemoryFact


class ConversationStore:
    def __init__(self, db_path: str = "conversations.db"):
        self.db_path = db_path
        self._initialize()

    def _connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self):
        with self._connect() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,

                    FOREIGN KEY (conversation_id)
                        REFERENCES conversations(id)
                        ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS conversation_memory (
                    conversation_id TEXT PRIMARY KEY,
                    summary TEXT NOT NULL,
                    facts TEXT NOT NULL,

                    FOREIGN KEY (conversation_id)
                        REFERENCES conversations(id)
                        ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS
                idx_messages_conversation
                ON messages(conversation_id);

                CREATE TABLE IF NOT EXISTS long_term_memories (
                    id TEXT PRIMARY KEY,
                    owner_id TEXT NOT NULL,
                    memory_key TEXT NOT NULL,
                    memory_value TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    source TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,

                    UNIQUE(owner_id, memory_key)
                );

                CREATE INDEX IF NOT EXISTS idx_memory_owner
                ON long_term_memories(owner_id);
            """)

    def create_conversation(self, conversation: Conversation):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO conversations (id, created_at)
                VALUES (?, ?)
                """,
                (conversation.id, conversation.created_at),
            )

    def add_message(self, conversation_id: str, message: Message):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO messages (
                    id, conversation_id, role, content, created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    message.id,
                    conversation_id,
                    message.role.value,
                    message.content,
                    message.created_at,
                ),
            )

    def get_messages(
        self,
        conversation_id: str,
        limit: int | None = None,
    ) -> list[Message]:

        with self._connect() as conn:
            if limit is None:
                rows = conn.execute(
                    """
                    SELECT * FROM messages
                    WHERE conversation_id = ?
                    ORDER BY created_at, rowid
                    """,
                    (conversation_id,),
                ).fetchall()
            else:
                if limit < 0:
                    raise ValueError("Limit cannot be negative.")

                rows = conn.execute(
                    """
                    SELECT * FROM (
                        SELECT * FROM messages
                        WHERE conversation_id = ?
                        ORDER BY created_at DESC, rowid DESC
                        LIMIT ?
                    )
                    ORDER BY created_at, rowid
                    """,
                    (conversation_id, limit),
                ).fetchall()

        return [
            Message(
                id=row["id"],
                role=MessageRole(row["role"]),
                content=row["content"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def save_memory(
        self,
        conversation_id: str,
        memory: ConversationMemory,
    ):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO conversation_memory (
                    conversation_id, summary, facts
                )
                VALUES (?, ?, ?)
                ON CONFLICT(conversation_id)
                DO UPDATE SET
                    summary = excluded.summary,
                    facts = excluded.facts
                """,
                (
                    conversation_id,
                    memory.summary,
                    json.dumps(memory.facts),
                ),
            )

    def get_memory(
        self,
        conversation_id: str,
    ) -> ConversationMemory:

        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT summary, facts
                FROM conversation_memory
                WHERE conversation_id = ?
                """,
                (conversation_id,),
            ).fetchone()

        if row is None:
            return ConversationMemory()

        return ConversationMemory(
            summary=row["summary"],
            facts=json.loads(row["facts"]),
        )


    def save_fact(self, owner_id: str, fact: MemoryFact):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO long_term_memories (
                    id,
                    owner_id,
                    memory_key,
                    memory_value,
                    confidence,
                    source,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)

                ON CONFLICT(owner_id, memory_key)
                DO UPDATE SET
                    memory_value = excluded.memory_value,
                    confidence = excluded.confidence,
                    source = excluded.source,
                    updated_at = excluded.updated_at
                """,
                (
                    fact.id,
                    owner_id,
                    fact.key,
                    fact.value,
                    fact.confidence,
                    fact.source,
                    fact.created_at,
                    fact.updated_at,
                ),
            )

    def get_facts(self, owner_id: str) -> list[MemoryFact]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM long_term_memories
                WHERE owner_id = ?
                ORDER BY updated_at DESC
                """,
                (owner_id,),
            ).fetchall()

        return [
            MemoryFact(
                id=row["id"],
                key=row["memory_key"],
                value=row["memory_value"],
                confidence=row["confidence"],
                source=row["source"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            for row in rows
        ]

    def delete_fact(self, owner_id: str, key: str):
        with self._connect() as conn:
            conn.execute(
                """
                DELETE FROM long_term_memories
                WHERE owner_id = ? AND memory_key = ?
                """,
                (owner_id, key),
            )
