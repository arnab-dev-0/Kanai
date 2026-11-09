import sqlite3
from pathlib import Path


class Database:

    def __init__(self, db_path: str | None = None):
        """Initialize the local SQLite database."""

        project_root = Path(__file__).resolve().parents[2]

        self.db_path = Path(db_path) if db_path else project_root / "data" / "kanai.db"

        # Create the database directory if it doesn't exist.
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.initialize_database()

    def get_connection(self) -> sqlite3.Connection:
        """Create and return a database connection."""

        connection = sqlite3.connect(self.db_path)

        # Return rows as dictionary-like objects.
        connection.row_factory = sqlite3.Row

        # Enable foreign key constraints.
        connection.execute("PRAGMA foreign_keys = ON")

        return connection

    def initialize_database(self) -> None:
        """Create database tables if they don't exist."""

        connection = self.get_connection()

        try:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL DEFAULT 'New conversation',
                    created_at TEXT NOT NULL DEFAULT (
                        datetime('now', '+5 hours', '+30 minutes')
                    ),
                    updated_at TEXT NOT NULL DEFAULT (
                        datetime('now', '+5 hours', '+30 minutes')
                    )
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL CHECK (
                        role IN ('user', 'assistant')
                    ),
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (
                        datetime('now', '+5 hours', '+30 minutes')
                    ),

                    FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                    ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS
                idx_messages_conversation_id
                ON messages(conversation_id);
                """)

            connection.commit()

        finally:
            connection.close()
