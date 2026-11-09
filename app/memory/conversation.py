import uuid

from app.memory.database import Database


class ConversationMemory:

    def __init__(self, conversation_id: str | None = None):
        """Initialize or resume a conversation."""

        self.database = Database()

        if conversation_id:
            self.conversation_id = conversation_id

            if not self._conversation_exists():
                raise ValueError(f"Conversation not found: {conversation_id}")

        else:
            self.conversation_id = str(uuid.uuid4())
            self._create_conversation()

    def _conversation_exists(self) -> bool:
        """Check whether a conversation exists."""

        connection = self.database.get_connection()

        try:
            result = connection.execute(
                """
                SELECT id FROM conversations
                WHERE id = ?
                """,
                (self.conversation_id,),
            ).fetchone()

            return result is not None

        finally:
            connection.close()

    def _create_conversation(self) -> None:
        """Create a new conversation in the database."""

        connection = self.database.get_connection()

        try:
            connection.execute(
                """
                INSERT INTO conversations (id)
                VALUES (?)
                """,
                (self.conversation_id,),
            )

            connection.commit()

        finally:
            connection.close()

    def add_message(self, role: str, content: str) -> None:
        """Save a message to the current conversation."""

        if role not in ("user", "assistant"):
            raise ValueError("Role must be either 'user' or 'assistant'.")

        if not isinstance(content, str) or not content.strip():
            raise ValueError("Message content cannot be empty.")

        connection = self.database.get_connection()

        try:
            connection.execute(
                """
                INSERT INTO messages (
                    conversation_id,
                    role,
                    content
                )
                VALUES (?, ?, ?)
                """,
                (self.conversation_id, role, content.strip()),
            )

            connection.execute(
                """
                UPDATE conversations
                SET updated_at = datetime('now', '+5 hours', '+30 minutes')
                WHERE id = ?
                """,
                (self.conversation_id,),
            )

            connection.commit()

        finally:
            connection.close()

    def get_history(self) -> list[dict[str, str]]:
        """Retrieve messages from the current conversation."""

        connection = self.database.get_connection()

        try:
            rows = connection.execute(
                """
                SELECT role, content
                FROM messages
                WHERE conversation_id = ?
                ORDER BY id ASC
                """,
                (self.conversation_id,),
            ).fetchall()

            return [{"role": row["role"], "content": row["content"]} for row in rows]

        finally:
            connection.close()

    def clear_history(self) -> None:
        """Delete all messages from the current conversation."""

        connection = self.database.get_connection()

        try:
            connection.execute(
                """
                DELETE FROM messages
                WHERE conversation_id = ?
                """,
                (self.conversation_id,),
            )

            connection.execute(
                """
                UPDATE conversations
                SET updated_at = datetime('now', '+5 hours', '+30 minutes')
                WHERE id = ?
                """,
                (self.conversation_id,),
            )

            connection.commit()

        finally:
            connection.close()

    def list_conversations(self) -> list[dict]:
        """Retrieve all existing conversations."""

        connection = self.database.get_connection()

        try:
            rows = connection.execute("""
                SELECT id, title, created_at, updated_at
                FROM conversations
                ORDER BY updated_at DESC, id DESC
                """).fetchall()

            return [dict(row) for row in rows]

        finally:
            connection.close()

    def delete_conversation(self) -> None:
        """Delete the current conversation and its messages."""

        connection = self.database.get_connection()

        try:
            connection.execute(
                """
                DELETE FROM conversations
                WHERE id = ?
                """,
                (self.conversation_id,),
            )

            connection.commit()

        finally:
            connection.close()
