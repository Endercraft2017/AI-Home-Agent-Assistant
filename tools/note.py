from agent.sqlite_helper import insert_note, get_note_by_id, update_note, delete_note
from agent.vector_helper import append_to_index, delete_from_index, search_vector
from agent.json_helper import save_single_id_value, load_single_id_value
from config import DEFAULT_TIME

def run(params):
    content = params.get("Content")
    action = params.get("Action") 
    if not content and action in ["set","get","update"]:
        return "Missing note content."
    if not action:
        return "No action is given"

    if action == "set":
        result = insert_note(content)
        if result == "success":
            return f"Note set: {content}"
        elif result == "There is an error":
            return result

    elif action == "update":
        old_note_id = load_single_id_value("note_id")
        new_content = content

        # Get old note content before updating
        result = update_note(old_note_id, new_content)

        if result != "success":
            return "Cannot find note to update"
        elif result == "There is an error":
            return result
        elif result == "Nothing to update":
            return "result"
        
        delete_from_index("note_index.pkl", old_note_id,"memory/history.db","notes")
        append_to_index("note_index.pkl", new_content, old_note_id, "notes")
        return "Note updated contents changed"

    elif action == "get":
        filtered_notes = []
        ids_by_content = None

        notes_by_content = search_vector(content,"note_index.pkl",3)
        ids_by_content = {rid for (_, rid) in notes_by_content}
        filtered_notes = [get_note_by_id(rid) for rid in ids_by_content]

        if not filtered_notes:
            return "No notes found"

        # Save the first note found (optional, or adjust as needed)
        note_id = filtered_notes[0][0]
        save_single_id_value("note_id", note_id)

        lines = [f"- {r[1]}" for r in filtered_notes]  # r[1]=content, r[3]=time
        return "Notes:\n" + "\n".join(lines)
    
    elif action == "delete":
        notes_by_content = []
        ids_by_content = []

        old_note_id = load_single_id_value("note_id")
        
        if content:
            notes_by_content = search_vector(content, "note_index.pkl", 1)
            ids_by_content = {row[1] for row in notes_by_content}
        
        if (old_note_id in ids_by_content):
            # Old ID and content have a common ID
            selected_id = old_note_id
        elif ids_by_content:
            # Fallback: use first from content search
            selected_id = next(iter(ids_by_content))
        else:
            return "No note provided to be cancelled"

        result = delete_note(selected_id)

        if result == "success":
            delete_from_index("note_index.pkl", selected_id)
            return "Note deleted"
        elif result == "There is an error":
            return result
        else:
            return "Cannot find note to delete"

    else:
        return "No valid action is given"

TOOL_LONG_DESCRIPTION = """
A tool to save, update, or retrieve or delete user notes.

Use this tool when the user wants to jot something down, recall what they've previously written, or modify the contents of an existing note.

Example use cases:

User: Make a note that I left my keys in the blue drawer  
User: Remember that my dog’s name is Coco  
User: Save a note saying I’m allergic to peanuts  
User: Do I have any notes about my gym routine?  
User: Can you find the note I left about car maintenance?  
User: What did I tell you yesterday about the meeting notes?  
User: Update my note about the neighbor — their name is actually Marie  
User: Change the note I wrote about the schedule, it’s on Friday now
"""

TOOL_SCHEMA = {
    "name": "Note",
        "description": "Set, update or get notes for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "Content": "Note content",
                "Action": {
                    "type": "string",
                    "description": "Choose if the user want to set, update or get a note",
                    "enum": ["set", "update", "get"]
                }
            },
            "required": ["Content", "Action"]
        }
}