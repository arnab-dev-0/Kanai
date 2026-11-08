
from google import genai
from google.genai import types

from app.llm.base import LLMProvider
from app.core.config import gemini_api_key, gemini_model


class GeminiProvider(LLMProvider):
    """
    Gemini implementation of the LLMProvider interface.
    """

    def __init__(self):
        if not gemini_api_key:
            raise ValueError(
                "KANAI_GEMINI_API_KEY is missing from .env"
            )

        self.client = genai.Client(api_key=gemini_api_key)
        self.model = gemini_model

    def generate_response(
        self,
        prompt: str,
        system_instruction: str
    ) -> str:
        """
        Generate a response using Gemini with a system instruction.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                )
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return response.text

        except Exception as error:
            raise RuntimeError(
                f"Gemini response generation failed: {error}"
            ) from error
