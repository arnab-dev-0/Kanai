
from app.llm.factory import create_llm_provider
from app.core.prompts import KANAI_SYSTEM_INSTRUCTION
from app.memory.conversation import ConversationMemory


def main():
    """
    Main entry point for Project Kanai.
    """

    print("\n🦚 Kanai is awake!")
    print("Your personal AI companion is ready.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    try:
        # Initialize LLM provider
        llm = create_llm_provider()

        print(f"Active provider: {type(llm).__name__}\n")

        # Initialize conversation memory
        memory = ConversationMemory()

        while True:

            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("\nKanai: Until we meet again! 🦚")
                break

            if user_input.lower() == "clear":
                memory.clear_history()
                print("\nKanai: Our conversation has been cleared.\n")
                continue

            try:
                # Store user message
                memory.add_message(
                    role="user",
                    content=user_input
                )

                # Generate response using complete conversation history
                response = llm.generate_response(
                    messages=memory.get_history(),
                    system_instruction=KANAI_SYSTEM_INSTRUCTION
                )

                # Store assistant response
                memory.add_message(
                    role="assistant",
                    content=response
                )

                print(f"\nKanai: {response}\n")

            except Exception as error:
                print(f"\nError generating response: {error}\n")

    except Exception as error:
        print(f"\nFailed to initialize Kanai: {error}")


if __name__ == "__main__":
    main()
