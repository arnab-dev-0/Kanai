
from app.core.config import provider

from app.llm.base import LLMProvider
from app.llm.gemini import GeminiProvider
from app.llm.openai import OpenAIProvider
from app.llm.ollama import OllamaProvider


def create_llm_provider(
    provider_name: str | None = None
) -> LLMProvider:
    """
    Create an LLM provider based on runtime selection
    or the default application configuration.
    """

    selected_provider = (
        provider_name or provider
    ).lower().strip()

    if selected_provider == "gemini":
        return GeminiProvider()

    elif selected_provider == "openai":
        return OpenAIProvider()

    elif selected_provider == "ollama":
        return OllamaProvider()

    else:
        raise ValueError(
            f"Unsupported LLM provider: {selected_provider}"
        )