from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Abstract base class for all LLM providers.

    Every provider must implement the generate_response() method.
    """

    @abstractmethod
    def generate_response(self, prompt: str, system_instruction: str) -> str:
        """
        Generate a response using the selected LLM provider.
        
        Args:
        prompt (str): User's message.
        system_instruction (str): Instructions defining the AI's behaviour.
        
        Returns:
        str: Generated response.
        """
        pass