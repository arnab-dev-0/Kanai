
from openai import OpenAI
from typing import cast
from openai.types.chat import ChatCompletionMessageParam

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
        messages: list[dict[str, str]],
        system_instruction: str
    ) -> str:
        """
        Generate a response using OpenAI with conversation history.
        """

        try:
            request_messages: list[ChatCompletionMessageParam] = [
                {
                    "role": "system",
                    "content": system_instruction
                }
            ]

            request_messages.extend(
                cast(
                    list[ChatCompletionMessageParam],
                    messages
                )
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=request_messages
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
