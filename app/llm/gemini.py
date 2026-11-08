
from google import genai
from google.genai import types

from app.core.config import gemini_api_key, gemini_model
from app.llm.base import LLMProvider


class GeminiProvider(LLMProvider):

    def __init__(self):
        if not gemini_api_key:
            raise ValueError("Gemini API key is missing.")

        self.client = genai.Client(
            api_key=gemini_api_key
        )

        self.model = gemini_model

    def generate_response(
        self,
        messages: list[dict[str, str]],
        system_instruction: str
    ) -> str:

        # Convert internal message format to Gemini format
        gemini_messages = [
            {
                "role": (
                    "model"
                    if message["role"] == "assistant"
                    else "user"
                ),
                "parts": [
                    {"text": message["content"]}
                ]
            }
            for message in messages
        ]

        response = self.client.models.generate_content(
            model=self.model,
            contents=gemini_messages,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )

        return response.text or ""
