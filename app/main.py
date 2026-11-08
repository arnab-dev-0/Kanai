
from app.llm.factory import create_llm_provider
from app.core.prompts import KANAI_SYSTEM_INSTRUCTION


def main():
    """
    Main entry point for Project Kanai.
    """

    print("\n🦚 Kanai is awake!")
    print("Your personal AI companion is ready.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    try:
        llm = create_llm_provider()

        print(f"Active provider: {type(llm).__name__}\n")

        while True:

            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("\nKanai: Until we meet again! 🦚")
                break

            try:
                response = llm.generate_response(
                    prompt=user_input,
                    system_instruction=KANAI_SYSTEM_INSTRUCTION
                )

                print(f"\nKanai: {response}\n")

            except Exception as error:
                print(f"\nError generating response: {error}\n")

    except Exception as error:
        print(f"\nFailed to initialize Kanai: {error}")


if __name__ == "__main__":
    main()
