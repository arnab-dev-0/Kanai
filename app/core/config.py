
import os
from dotenv import load_dotenv

load_dotenv()

# LLM provider
provider = os.getenv("KANAI_LLM_PROVIDER", "gemini")

# Gemini configuration
gemini_api_key = os.getenv("KANAI_GEMINI_API_KEY")
gemini_model = os.getenv(
    "KANAI_GEMINI_MODEL",
    "gemini-2.5-flash"
    )

# OpenAI configuration
openai_api_key = os.getenv("KANAI_OPENAI_API_KEY")
openai_model = os.getenv(
    "KANAI_OPENAI_MODEL",
    "gpt-6-luna"
)

# Ollama configuration
ollama_base_url = os.getenv(
    "KANAI_OLLAMA_BASE_URL",
    "http://localhost:11434"
)

ollama_model = os.getenv(
    "KANAI_OLLAMA_MODEL", "mistral"
)