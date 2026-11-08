
from ollama import Client

from app.llm.base import LLMProvider
from app.core.config import ollama_base_url, ollama_model


class OllamaProvider(LLMProvider):
    """
    Ollama implementation of the LLMProvider interface.
    """

    def __init__(self):
        if not ollama_model:
            raise ValueError(
                "KANAI_OLLAMA_MODEL is missing from .env"
            )

        self.client = Client(host=ollama_base_url)
        self.model = ollama_model

    def generate_response(
        self,
        messages: list[dict[str, str]],
        system_instruction: str
    ) -> str:
        """
        Generate a response using Ollama with conversation history.
        """

        try:
            conversation = [
                {
                    "role": "system",
                    "content": system_instruction
                }
            ]

            conversation.extend(messages)

            response = self.client.chat(
                model=self.model,
                messages=conversation
            )

            content = response.message.content

            if not content:
                raise RuntimeError(
                    "Ollama returned an empty response."
                )

            return content

        except Exception as error:
            raise RuntimeError(
                f"Ollama response generation failed: {error}"
            ) from error
