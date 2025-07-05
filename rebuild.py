from agent.vector_helper import build_tool_index, build_memory_index

print("Rebuilding all vector indexes...")
build_tool_index()
build_memory_index("memory/assistant.db", "notes", "content", "note_index.pkl")
build_memory_index("memory/assistant.db", "reminders", "content", "reminder_index.pkl")
print("✅ All indexes rebuilt.")
