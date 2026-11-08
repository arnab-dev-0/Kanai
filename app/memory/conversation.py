
class ConversationMemory:

    def __init__(self):
        """Initialize an empty conversation history."""
        self.messages = []

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""

        if role not in ("user", "assistant"):
            raise ValueError(
                "Role must be either 'user' or 'assistant'."
            )

        if not isinstance(content, str) or not content.strip():
            raise ValueError("Message content cannot be empty.")

        message = {
            "role": role,
            "content": content.strip()
        }

        self.messages.append(message)

    def get_history(self) -> list[dict[str, str]]:
        """Return a copy of the conversation history."""

        return self.messages.copy()

    def clear_history(self) -> None:
        """Clear all conversation messages."""

        self.messages.clear()
