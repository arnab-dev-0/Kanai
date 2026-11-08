
from app.llm.factory import create_llm_provider


def main():

    # Choose any provider at runtime
    llm = create_llm_provider("openai")  # Options: "gemini", "openai", "ollama"

    print("Selected provider:", type(llm).__name__)

    response = llm.generate_response(
        "Introduce yourself as Kanai."
    )

    print("Kanai:", response)


if __name__ == "__main__":
    main()