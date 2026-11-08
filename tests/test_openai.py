
from app.llm.openai import OpenAIProvider
from app.core.prompts import KANAI_SYSTEM_INSTRUCTION


def main():
    kanai = OpenAIProvider()

    response = kanai.generate_response(
        prompt="Introduce yourself. What is your name?",
        system_instruction=KANAI_SYSTEM_INSTRUCTION
    )

    print("Kanai:", response)


if __name__ == "__main__":
    main()
