
from app.llm.factory import create_llm_provider
from app.core.prompts import KANAI_SYSTEM_INSTRUCTION
from app.memory.conversation import ConversationMemory


def display_conversations(memory):

    conversations = memory.list_conversations()

    if not conversations:
        print("\nNo previous conversations found.\n")
        return

    print("\nYour conversations:\n")

    for conversation in conversations:
        print(f"ID: {conversation['id']}")
        print(f"Created: {conversation['created_at']}")
        print(f"Updated: {conversation['updated_at']}")
        print("-" * 50)


def select_conversation():

    memory_manager = ConversationMemory()

    # Remove the automatically created empty conversation.
    memory_manager.delete_conversation()

    while True:

        print("""
Choose an option:

1. Resume a conversation
2. Start a new conversation
3. Exit
""")

        choice = input("Your choice: ").strip()

        if choice == "1":

            display_conversations(memory_manager)

            conversation_id = input(
                "\nEnter conversation ID: "
            ).strip()

            try:
                memory = ConversationMemory(
                    conversation_id=conversation_id
                )

                print("\nConversation resumed successfully.")
                print(f"Conversation ID: {memory.conversation_id}\n")

                return memory

            except ValueError as error:
                print(f"\nError: {error}\n")

        elif choice == "2":

            memory = ConversationMemory()

            print("\nStarted a new conversation.")
            print(f"Conversation ID: {memory.conversation_id}\n")

            return memory

        elif choice == "3":

            print("\nKanai: Until we meet again! 🦚")
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
                print("\nKanai: Until we meet again! 🦚")
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

                display_conversations(memory)
                continue

            elif command == "resume":

                conversation_id = input(
                    "Enter conversation ID: "
                ).strip()

                try:
                    memory = ConversationMemory(
                        conversation_id=conversation_id
                    )

                    print("\nConversation resumed successfully.")
                    print(f"Conversation ID: {memory.conversation_id}\n")

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
                        print("\nKanai: Until we meet again! 🦚")
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
