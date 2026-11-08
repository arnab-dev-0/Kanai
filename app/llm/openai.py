
from openai import OpenAI

from app.llm.base import LLMProvider
from app.core.config import openai_api_key, openai_model


class OpenAIProvider(LLMProvider):
    """
    OpenAI implementation of the LLMProvider interface.
    """

    def __init__(self):
        if not openai_api_key:
            raise ValueError(
                "KANAI_OPENAI_API_KEY is missing from .env"
            )

        self.client = OpenAI(api_key=openai_api_key)
        self.model = openai_model

    def generate_response(
        self,
        prompt: str,
        system_instruction: str
    ) -> str:
        """
        Generate a response using OpenAI with a system instruction.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_instruction
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            content = response.choices[0].message.content

            if not content:
                raise RuntimeError(
                    "OpenAI returned an empty response."
                )

            return content

        except Exception as error:
            raise RuntimeError(
                f"OpenAI response generation failed: {error}"
            ) from error
