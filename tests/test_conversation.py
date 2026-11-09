
from app.memory.conversation import ConversationMemory


# Create a new conversation
memory = ConversationMemory()

conversation_id = memory.conversation_id

print("Conversation ID:", conversation_id)

# Add messages
memory.add_message("user", "My name is Arnab.")

memory.add_message(
    "assistant",
    "Nice to meet you, Arnab!"
)

# Retrieve messages
print("\nFirst conversation history:")
print(memory.get_history())


# Simulate application restart
del memory

# Resume the same conversation
memory = ConversationMemory(
    conversation_id=conversation_id
)

print("\nRestored conversation history:")
print(memory.get_history())


# List conversations
print("\nAll conversations:")
print(memory.list_conversations())
