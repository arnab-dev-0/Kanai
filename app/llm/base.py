from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Abstract base class for all LLM providers.

    Every provider must implement the generate_response() method.
    """

    @abstractmethod
    def generate_response(
        self, messages: list[dict[str, str]], system_instruction: str
    ) -> str:
        """
        Generate a response using conversation history.

        Args:
        messages: List of user and assistant messages.
        system_instruction: Instructions defining Kanai's behavior.

        Returns:
        Generated assistant response.
        """
        pass
