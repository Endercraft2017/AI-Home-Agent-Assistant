import json
import os

from config import MAX_CONVERSATION_HISTORY
from .sqlite_helper import insert_conversation_pair

JSON_MEMORY_FILE = "memory/conversation_memory.json"
GET_ID_FILE = "memory/get_id.json"

def save_conversation_json(user_text, response_text,tool, memory_file=JSON_MEMORY_FILE, max_json=MAX_CONVERSATION_HISTORY):
    # Load existing data or start new list
    if os.path.exists(memory_file):
        with open(memory_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append new conversation
    data.append({"user": user_text, "assistant": response_text, "tool": tool})

    # If more than max_json, move the oldest to text file and shift
    while len(data) > max_json:
        oldest = data.pop(0)
        insert_conversation_pair(oldest["user"],oldest["assistant"])

    # Save back to JSON file
    with open(memory_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_conversations_json(memory_file=JSON_MEMORY_FILE):
    if not os.path.exists(memory_file):
        return []
    with open(memory_file, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
        
### For formatting the chat history
def format_conversation_history(conversations, max_turns=MAX_CONVERSATION_HISTORY):
    """
    Format the last `max_turns` of chat history for context.
    """
    blocks = []
    for convo in conversations[-max_turns:]:
        user = convo.get("user", "").strip()
        reply = convo.get("assistant", "").strip()
        blocks.append(f"User: {user}\nAssistant: {reply}")
    return "\n\n".join(blocks)

### For saving and loading the last "get" reminder

def save_single_id_value(key, value, file_path=GET_ID_FILE):
    # Load existing data or start new dict
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    # Update only the specified key
    data[key] = value
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_single_id_value(key, file_path=GET_ID_FILE):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data.get(key)
        except json.JSONDecodeError:
            return None