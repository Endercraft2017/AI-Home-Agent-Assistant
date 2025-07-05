import sqlite3
from datetime import datetime
import json

from .vector_helper import append_to_index

DB_PATH = "memory/history.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            remind_at_date TEXT,
            remind_at_time TEXT,
            status TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            content TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

###Use this for inserting conversations to the DB
def insert_conversation_pair(user_input, reply):
    pair = {
        "User": user_input,
        "Assistant": reply
    }
    insert_memory_log("conversation", json.dumps(pair))

def insert_memory_log(entry_type, content):
    with get_connection() as conn:
        cursor = conn.execute("INSERT INTO memory_log (type, content) VALUES (?, ?)", (entry_type, content))
        note_id = cursor.lastrowid
        conn.commit()
    append_to_index("memory_index.pkl", content, note_id, "memory")


### Reminder functions

def insert_reminder(content, date, time, status = "active"):
    try:
        with get_connection() as conn:
            cursor = conn.execute("INSERT INTO reminders (content, remind_at_date, remind_at_time, status) VALUES (?, ?, ?, ?)", (content, date, time, status))
            reminder_id = cursor.lastrowid
            conn.commit()
        result = append_to_index("reminder_index.pkl", content, reminder_id, "reminders")
        return "Success"
    except Exception as e:
        print(f"[ERROR] sqlite_helper.insert_reminder: {e}")
        return f"Failed to add reminder, here is the error:\n {e}"

def update_reminder(reminder_id, new_content=None, new_date=None, new_time=None, new_status=None):
    try:
        with get_connection() as conn:
            fields = []
            values = []

            if new_content:
                fields.append("content = ?")
                values.append(new_content)
            if new_date:
                fields.append("remind_at_date = ?")
                values.append(new_date)
            if new_time:
                fields.append("remind_at_time = ?")
                values.append(new_time)
            if new_status:
                fields.append("status = ?")
                values.append(new_status)

            if not fields:
                return "Nothing to update"  # Nothing to update

            values.append(reminder_id)
            query = f"UPDATE reminders SET {', '.join(fields)} WHERE id = ?"
            conn.execute(query, tuple(values))
            conn.commit()
            return "success"
    except Exception as e:
        print(f"[ERROR] sqlite_helper.update_reminder: {e}")
        return "There is an error"

def get_reminder_by_id(reminder_id):
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM reminders WHERE id = ? AND status != 'cancelled'", (reminder_id,))
        return cursor.fetchone()

def get_reminders_by_date(date):
    with get_connection() as conn:
        c = conn.cursor()
        day, month, year = date.split("-")
        if day == "00" and month == "00":
            # Yearly
            c.execute("SELECT * FROM reminders WHERE substr(remind_at_date, 7, 4) = ? AND status != 'cancelled'", (year,))
        elif day == "00":
            # Monthly
            c.execute("SELECT * FROM reminders WHERE substr(remind_at_date, 4, 2) = ? AND substr(remind_at_date, 7, 4) = ? AND status != 'cancelled'", (month, year))
        else:
            # Specific day
            c.execute("SELECT * FROM reminders WHERE remind_at_date = ? AND status != 'cancelled'", (date,))
        return c.fetchall()

def get_all_reminders():  # get all reminders with the latest first
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM reminders WHERE status != 'cancelled' ORDER BY remind_at_date, remind_at_time")
        return cursor.fetchall()

## Not yet implemented
def delete_reminder(reminder_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        conn.commit()

### Note functions

def insert_note(content):
    try:
        with get_connection() as conn:
            cursor = conn.execute("INSERT INTO notes (content) VALUES (?)", (content,))
            note_id = cursor.lastrowid
            conn.commit()
        append_to_index("note_index.pkl", content, note_id, "notes")
        return "success"
    except Exception as e:
        print(f"[ERROR] sqlite_helper.insert_note: {e}")
        return "There is an error"

def update_note(note_id, new_content):
    try:
        with get_connection() as conn:
            conn.execute("UPDATE notes SET content = ? WHERE id = ?", (new_content, note_id))
            conn.commit()
            return "success"
    except Exception as e:
        print(f"[ERROR] sqlite_helper.update_note: {e}")
        return "There is an error"

def get_note_by_id(note_id):
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        return cursor.fetchone()

def get_all_notes():
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM notes ORDER BY created_at DESC")
        return cursor.fetchall()

def delete_note(note_id):
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            conn.commit()
        return "success"
    except Exception as e:
        print(f"[ERROR] sqlite_helper.delete_note: {e}")
        return "There is an error"