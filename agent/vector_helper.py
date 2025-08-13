import os
import pickle
import numpy as np
import faiss
import sqlite3
from .llm import embed_text

INDEX_DIR = "memory"
EMBEDDING_DIM = 1024

os.makedirs(INDEX_DIR, exist_ok=True)

 ## consider changing vector db options, ask chat gpt to convert all these functions to a vector db that has a delete and update function

### Tool Embeddings
def build_tool_index():
    from tools import ALL_TOOLS
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    id_map = []
    for name, module in ALL_TOOLS.items():
        desc = module.TOOL_LONG_DESCRIPTION
        vec = np.array([embed_text(desc)], dtype="float32")
        index.add(vec)
        id_map.append(name)
    with open(f"{INDEX_DIR}/tool_index.pkl", "wb") as f:
        pickle.dump({"index": index, "id_map": id_map}, f)

def search_tool(prompt, top_k=1):
    with open(f"{INDEX_DIR}/tool_index.pkl", "rb") as f:
        data = pickle.load(f)
    index = data["index"]
    id_map = data["id_map"]
    vec = np.array([embed_text(prompt)], dtype="float32")
    D, I = index.search(vec, top_k)
    return id_map[I[0][0]]

###Building Contextual Query for tools
def is_followup(message: str) -> bool:
    message = message.lower().strip()
    followup_starts = ("what about","how about","and","also","what else","more about","that too","can you also","let's add","include","add that too","continue with","follow up with","as well","do the same for","like before","just like that","same for","similar to that","another one","next one","that again","repeat for","same thing but","now do","in addition","okay then","alright then","back to that",)
    return message.startswith(followup_starts)

def is_followup_request(message: str) -> bool:
    message = message.lower().strip()

    # Key phrases that signal a follow-up prompt
    followup_phrases = (
        "would you like me to","do you want me to","should i also","should i go ahead and","want me to","is that okay","would that be fine","shall i","do you also want","do you want to","need me to","would you like to","should we","need help with the rest","should i repeat that","should i apply that","need to adjust","should i set","want to change","should we continue","can i update","can i add","shall we add","should i modify","should we change","let me know if","let me know what","tell me if","anything else you need","want me to handle that too","would you like to continue","should i do the same","can i help with that","should i fix that as well","want me to fix that","need me to change it","can i assist you further","want to proceed"
    )

    for phrase in followup_phrases:
        if phrase in message:
            return True

    # Basic question detection for soft prompts
    if message.endswith("?") and any(word in message for word in ("should", "want", "like", "can", "shall", "need", "continue", "help", "add")):
        return True

    return False


def build_contextual_query(user_input, last_chat) -> str:
    followup = is_followup(user_input)
    print(f"[DEBUG] followup vector_helper.py: {followup}")

    # No follow-up detected → return as-is
    if not followup:
        return user_input

    # No tool previously used → skip attaching context
    if last_chat["tool"] == "NONE":
        return user_input

    # Standard follow-up: attach the last user query
    return f"Following up on '{last_chat['user']}': {user_input}"

def build_contextual_query_followup(user_input, last_chat) -> str:
    followup = is_followup(user_input)
    followup_request = is_followup_request(user_input)
    print(f"[DEBUG] followup vector_helper.py: {followup}, request: {followup_request}")

    # No follow-up detected → return as-is
    if not followup and not followup_request:
        return user_input

    # No tool previously used → skip attaching context unless it's a follow-up request
    if last_chat["tool"] == "NONE" and not followup_request:
        return user_input

    # If the assistant asked a follow-up (request), include both user & assistant context
    if followup_request and last_chat["tool"] == "NONE":
        return f"Assistant said: '{last_chat['assistant']}' \n User: {user_input}"

    if followup_request and last_chat["tool"] != "NONE":
        return f"""
        Following up on conversation:
        User said: '{last_chat['user']}'
        Assistant said: '{last_chat['assistant']}'

        User Now: {user_input}""" 

    # Standard follow-up: attach the last user query
    return f"Following up on '{last_chat['user']}': {user_input}"

### Memory Embeddings
def build_memory_index(db_path, table, column="content", out_file="memory_index.pkl"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(f"SELECT id, {column} FROM {table}")
    rows = c.fetchall()
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    id_map = []
    for row_id, text in rows:
        vec = np.array([embed_text(text)], dtype="float32")
        index.add(vec)
        id_map.append((table, row_id))  # Track which table it came from
    with open(f"{INDEX_DIR}/{out_file}", "wb") as f:
        pickle.dump({"index": index, "id_map": id_map}, f)

def search_memory(prompt, index_file="memory_index.pkl", top_k=3):
    with open(f"{INDEX_DIR}/{index_file}", "rb") as f:
        data = pickle.load(f)
    index = data["index"]
    id_map = data["id_map"]
    vec = np.array([embed_text(prompt)], dtype="float32")
    D, I = index.search(vec, top_k)
    return [id_map[i] for i in I[0]]  # (table, row_id)

### Reminder Embeddings
def build_reminder_index(db_path, table, column="content", out_file="reminder_index.pkl"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(f"SELECT id, {column} FROM {table}")
    rows = c.fetchall()
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    id_map = []
    for row_id, text in rows:
        embedding = embed_text(text)
        vec = np.array([embed_text(text)], dtype="float32")
        index.add(vec)
        id_map.append((table, row_id, embedding))  # Track which table it came from
    with open(f"{INDEX_DIR}/{out_file}", "wb") as f:
        pickle.dump({"index": index, "id_map": id_map}, f)

def search_vector(prompt, index_file="reminder_index.pkl", top_k=3, threshold=0.5):

    # Load FAISS index and ID mapping
    with open(f"{INDEX_DIR}/{index_file}", "rb") as f:
        data = pickle.load(f)
    index = data["index"]
    id_map = data["id_map"]

    # Get query embedding
    query_vec = np.array([embed_text(prompt)], dtype="float32")
    D, I = index.search(query_vec, top_k)

    results = []
    for i, dist in zip(I[0], D[0]):
        if i >= len(id_map):
            continue
        content, row_id, embedding = id_map[i]
        content_vec = np.array(embedding, dtype="float32")
        # Cosine similarity (instead of FAISS distance)
        similarity = np.dot(query_vec[0], content_vec) / (
            np.linalg.norm(query_vec[0]) * np.linalg.norm(content_vec)
        )
        if similarity >= threshold:
            results.append((content, row_id))  # Return as tuple like before
        #print(f"[DEBUG] vector_helper.search_vector: {similarity}")

    return results

def search_and_fetch(prompt, db_path, table, column="content", top_k=3, index_file=None):
    if index_file is None:
        index_file = f"{table}_index.pkl"

    ids = search_memory(prompt, index_file, top_k)

    results = []
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for tbl, row_id in ids:
        if tbl == table:
            c.execute(f"SELECT id, {column} FROM {table} WHERE id = ?", (row_id,))
            row = c.fetchone()
            if row:
                results.append({"id": row[0], "content": row[1]})
    return results

#Use this to search reminders and get content
def get_reminder(prompt, db_path="memory/history.db", top_k=3):
    return search_and_fetch(prompt, db_path, table="reminders", column="content", index_file="reminder_index.pkl")

#Use this to search chat history and get content
def get_chat_history(prompt, db_path="memory/history.db", top_k=3):
    return search_and_fetch(prompt, db_path, table="chat_history", column="content", index_file="chat_index.pkl")


#Add to vector db index
def append_to_index(index_file, text, row_id, table):
    try:
        with open(f"{INDEX_DIR}/{index_file}", "rb") as f:
            data = pickle.load(f)
            index = data["index"]
            meta = data["id_map"]
    #except FileNotFoundError:
    except Exception as e:
        print(f"[DEBUG] vector_helper.py: {e}")
        # Initialize new index if it doesn't exist
        dim = EMBEDDING_DIM
        index = faiss.IndexFlatL2(dim)
        meta = []

    try:
        embedding = embed_text(text)
        vector = np.array([embedding], dtype='float32')
        index.add(vector)
        meta.append((text, row_id, embedding))

        with open(f"{INDEX_DIR}/{index_file}", "wb") as f:
            pickle.dump({"index": index, "id_map": meta}, f)
        return "Embedding complete"
    except Exception as e:
        print(e)
        return e

### Delete from index

def delete_from_index_with_table(index_file, row_id, table):
    try:
        with open(f"{INDEX_DIR}/{index_file}", "rb") as f:
            data = pickle.load(f)
            index = data["index"]
            meta = data["id_map"]
    except FileNotFoundError:
        print(f"[delete_from_index] Index file {index_file} not found.")
        return False

    # Find indices to keep (not matching the row_id and table)
    keep_indices = [i for i, (tbl, rid) in enumerate(meta) if not (tbl == table and rid == row_id)]

    if len(keep_indices) == len(meta):
        print(f"[delete_from_index] No entry found for table={table}, row_id={row_id}")
        return False

    # Rebuild index and meta
    if keep_indices:
        # Get all vectors from the index
        all_vecs = faiss.vector_to_array(index.reconstruct_n(0, index.ntotal)).reshape(index.ntotal, -1)
        new_vecs = all_vecs[keep_indices]
        dim = new_vecs.shape[1]
        new_index = faiss.IndexFlatL2(dim)
        new_index.add(new_vecs)
        new_meta = [meta[i] for i in keep_indices]
    else:
        # No items left
        dim = index.d
        new_index = faiss.IndexFlatL2(dim)
        new_meta = []

    with open(f"{INDEX_DIR}/{index_file}", "wb") as f:
        pickle.dump({"index": new_index, "id_map": new_meta}, f)

    return True

def delete_from_index(index_file, row_id, db_path="memory/history.db", table="reminders", column="content"):
    try:
        with open(f"{INDEX_DIR}/{index_file}", "rb") as f:
            data = pickle.load(f)
            index = data["index"]
            meta = data["id_map"]

        # Remove the entry with the given row_id
        meta = [m for m in meta if m[1] != row_id]

        # Rebuild the index with the remaining items
        new_index = faiss.IndexFlatL2(index.d)
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        for tbl, rid, embedding in meta:
            c.execute(f"SELECT {column} FROM {table} WHERE id = ?", (rid,))
            result = c.fetchone()
            if result:
                text = result[0]
                vec = np.array([embedding], dtype="float32")
                new_index.add(vec)
        conn.close()

        with open(f"{INDEX_DIR}/{index_file}", "wb") as f:
            pickle.dump({"index": new_index, "id_map": meta}, f)
    except Exception as e:
        print(f"⚠️ Error deleting from index: {e}")