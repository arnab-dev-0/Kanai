
from app.llm.factory import create_llm_provider
from app.core.prompts import KANAI_SYSTEM_INSTRUCTION
from app.memory.conversation import ConversationMemory


def display_conversations() -> list[dict]:
    """Display conversations with numbered selection."""

    conversations = ConversationMemory.list_all_conversations()

    if not conversations:
        print("\nNo previous conversations found.\n")
        return []

    print("\nYour conversations:\n")

    for index, conversation in enumerate(conversations, start=1):

        title = conversation["title"] or "Untitled Conversation"

        print(f"{index}. {title}")
        print(f"   Last updated: {conversation['updated_at']}")
        print("-" * 50)

    return conversations


def select_conversation():
    """Allow the user to resume or start a conversation."""

    while True:

        print("""
Choose an option:

1. Resume a conversation
2. Start a new conversation
3. Exit
""")

        choice = input("Your choice: ").strip()

        if choice == "1":

            conversations = display_conversations()

            if not conversations:
                continue

            selection = input(
                "\nChoose a conversation number (0 to go back): "
            ).strip()

            if selection == "0":
                continue

            if not selection.isdigit():
                print("\nInvalid input. Please enter a valid number.\n")
                continue

            index = int(selection)

            if index < 1 or index > len(conversations):
                print("\nInvalid conversation number. Please try again.\n")
                continue

            conversation_id = conversations[index - 1]["id"]

            try:
                memory = ConversationMemory(
                    conversation_id=conversation_id
                )

                print("\nConversation resumed successfully.")
                print(
                    f"Conversation: "
                    f"{conversations[index - 1]['title'] or 'Untitled Conversation'}"
                )
                print()

                return memory

            except ValueError as error:
                print(f"\nError: {error}\n")

        elif choice == "2":

            memory = ConversationMemory()

            print("\nStarted a new conversation.")
            print(f"Conversation ID: {memory.conversation_id}\n")

            return memory

        elif choice == "3":

            print("\nKanai: Goodbye! Until we meet again! 🦚")
            return None

        else:
            print("\nInvalid choice. Please try again.\n")


def main():

    print("\n🦚 Kanai is awake!")
    print("Your personal AI companion is ready.\n")

    try:

        llm = create_llm_provider()

        print(f"Active provider: {type(llm).__name__}")

        memory = select_conversation()

        if memory is None:
            return

        while True:

            user_input = input("You: ").strip()

            if not user_input:
                continue

            command = user_input.lower()

            if command in ["exit", "quit"]:

                print("\nKanai: Goodbye! Until we meet again! 🦚")
                break

            elif command == "help":

                print("""
Available commands:

new     - Start a new conversation
list    - List previous conversations
resume  - Resume a conversation
clear   - Clear current conversation
delete  - Delete current conversation
exit    - Exit Kanai
""")
                continue

            elif command == "new":

                memory = ConversationMemory()

                print("\nStarted a new conversation.")
                print(f"Conversation ID: {memory.conversation_id}\n")
                continue

            elif command == "list":

                display_conversations()
                continue

            elif command == "resume":

                conversations = display_conversations()

                if not conversations:
                    continue

                selection = input(
                    "\nChoose a conversation number (0 to cancel): "
                ).strip()

                if selection == "0":
                    continue

                if not selection.isdigit():
                    print("\nInvalid input. Please enter a valid number.\n")
                    continue

                index = int(selection)

                if index < 1 or index > len(conversations):
                    print("\nInvalid conversation number. Please try again.\n")
                    continue

                conversation_id = conversations[index - 1]["id"]

                try:
                    memory = ConversationMemory(
                        conversation_id=conversation_id
                    )

                    print("\nConversation resumed successfully.")
                    print(
                        f"Conversation: "
                        f"{conversations[index - 1]['title'] or 'Untitled Conversation'}"
                    )
                    print()

                except ValueError as error:
                    print(f"\nError: {error}\n")

                continue

            elif command == "clear":

                memory.clear_history()

                print("\nKanai: Current conversation history cleared.\n")
                continue

            elif command == "delete":

                confirmation = input(
                    "Permanently delete this conversation? (yes/no): "
                ).strip().lower()

                if confirmation == "yes":

                    memory.delete_conversation()

                    print("\nConversation deleted.")

                    memory = select_conversation()

                    if memory is None:
                        break

                else:
                    print("\nDeletion cancelled.\n")

                continue

            try:

                memory.add_message(
                    role="user",
                    content=user_input
                )

                response = llm.generate_response(
                    messages=memory.get_history(),
                    system_instruction=KANAI_SYSTEM_INSTRUCTION
                )

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
