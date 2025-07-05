# ask_memory.py

from agent.vector_helper import search_chat_history, search_reminders

print("🧠 Ask your memory (e.g., 'Did I mention dentist?')\n")
user_input = input("🔎 Query: ")

print("\n🔽 Searching reminders...")
matches = search_reminders(user_input)
for m in matches:
    print("📌 Reminder:", m["content"])

print("\n🔽 Searching chat history...")
matches = search_chat_history(user_input)
for m in matches:
    print("💬 Chat:", m["content"])