from app.memory.conversation import ConversationMemory

memory = ConversationMemory()

memory.add_message("user", "Hello Kanai!")
memory.add_message("assistant", "Hello! How are you?")

print(memory.get_history())

memory.clear_history()

print(memory.get_history())