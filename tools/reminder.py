from agent.sqlite_helper import get_reminders_by_date, insert_reminder, get_reminder_by_id, update_reminder
from agent.vector_helper import append_to_index, delete_from_index, search_vector
from agent.json_helper import save_single_id_value, load_single_id_value
from config import DEFAULT_TIME

def run(params):
    content = params.get("Content")
    date = params.get("Date")
    time = params.get("Time")
    status = params.get("Status")
    if date == "00-00-00":
        date = ""
    if time == "00:00":
        time = ""
    if time == "":
        time = DEFAULT_TIME
    action = params.get("Action") 
    if not content and action == "set" :
        return "Missing reminder content."
    if not action:
        return "No action is given"

    if action == "set":
        result = insert_reminder(content,date,time)
        if result == "Success":
            return f"Reminder set: '{content}' at {f'{date} {time}'}"
        else:
            return result

    elif action == "update":
        old_reminder_id = load_single_id_value("reminder_id")
        old = []
        new_content = None
        new_date = None
        new_time = None

        if content:
            new_content = content
        if date:
            new_date = date
        if time:
            new_time = time

        # Get old reminder content before updating
        if old_reminder_id:
            old = get_reminder_by_id(old_reminder_id)
        result = update_reminder(old_reminder_id, new_content, new_date, new_time)

        if result != "success":
            return "Cannot find reminder to update"
        elif result == "There is an error":
            return result
        elif result == "Nothing to update":
            return "result"
        
        if (not content) and (date or time):
            return "Reminder updated no change in content"
        delete_from_index("reminder_index.pkl", old_reminder_id,"memory/history.db","reminders")
        append_to_index("reminder_index.pkl", new_content or old[1], old_reminder_id, "reminders")
        return "Reminder updated contents changed"

    elif action == "get":
        filtered_reminders = []
        ids_by_date = None
        ids_by_content = None
        common_ids = None

        if not date and not content:
            return "No date or content provided, need to provide"
        if date:
            reminders_by_date = get_reminders_by_date(date)
            ids_by_date = {row[0] for row in reminders_by_date}
        if content:
            reminders_by_content = search_vector(content,"reminder_index.pkl",3)
            ids_by_content = {rid for (_, rid) in reminders_by_content}
        if ids_by_date and ids_by_content:
            common_ids = ids_by_date & ids_by_content

        if date:
            filtered_reminders = reminders_by_date
        else:
            # Fetch full rows for these IDs
            filtered_reminders = [get_reminder_by_id(rid) for rid in ids_by_content]
        
        if common_ids:
            # Return only reminders present in both (full rows)
            filtered_reminders = [row for row in reminders_by_date if row[0] in common_ids]

        if not filtered_reminders:
            return "No reminders found"

        # Save the first reminder_id found (optional, or adjust as needed)
        reminder_id = filtered_reminders[0][0]
        save_single_id_value("reminder_id", reminder_id)

        lines = [f"- {r[1]} at {r[3]}" for r in filtered_reminders]  # r[1]=content, r[3]=time
        return "Reminders:\n" + "\n".join(lines)
    
    elif action == "cancel":
        reminders_by_date = []
        ids_by_date = []
        reminders_by_content = []
        ids_by_content = []
        ids_all = []

        old_reminder_id = load_single_id_value("reminder_id")
        
        if date:
            reminders_by_date = get_reminders_by_date(date)
            ids_by_date = {row[0] for row in reminders_by_date}
        if content:
            reminders_by_content = search_vector(content, "reminder_index.pkl", 1)
            ids_by_content = {row[1] for row in reminders_by_content}
        if old_reminder_id and ids_by_date and ids_by_content:
            ids_all = {old_reminder_id} & ids_by_date & ids_by_content
        
        if ids_all:
            # All three have a common ID
            selected_id = ids_all.pop()
        elif (old_reminder_id in ids_by_date):
            # Old ID and date have a common ID
            selected_id = old_reminder_id
        elif (old_reminder_id in ids_by_content):
            # Old ID and content have a common ID
            selected_id = old_reminder_id
        elif ids_by_content:
            # Fallback: use first from content search
            selected_id = next(iter(ids_by_content))
        elif (ids_by_date and ids_by_content):
            # Date and content have a common ID
            selected_id = (ids_by_date & ids_by_content).pop()
        else:
            return "No reminder provided to be cancelled"

        # Get old reminder content before updating
        result = update_reminder(selected_id, None, None, None,"cancelled")

        if result == "success":
            delete_from_index("reminder_index.pkl", selected_id)
            return "Reminder Cancelled"
        if result == "There is an error":
            return result
        else:
            return "Cannot find reminder to cancel"
    else:
        return "No valid action is given"

TOOL_LONG_DESCRIPTION = """
A tool to set, update, retrieve, or cancel reminders for the user.

Use this tool whenever the user asks to create a new reminder, modify an existing one, check for upcoming reminders, or cancel a scheduled reminder.

Example use cases:

User: Add a reminder for going to the dentist tomorrow at 3 PM  
User: Set a reminder for my dinner later at 7 PM  
User: I need a reminder for...  
User: Remind me about my meeting  
User: Can you cancel my reminder for the vet?  
User: Do I have a reminder set for tomorrow?  
User: Can you check if I already set a reminder for the 3rd?  
User: I need you to change my reminder from 5 PM to 6 PM  
User: Can you update my reminder to say "project deadline" instead?
"""

ADDITIONAL_INSTRUCTION = """
In the reminder details include the whole intent of the user. Make sure to include all the details.
For Date and time, use the format DD-MM-YYYY and HH:MM. And put 00 on unknown fields if the user did not specify the day, month, or time.
Add 2 hours to the current time if the user says 'later'.
For the Content use the whole intent of the user in a way that it is a statement not an action.
If the user wants to get a reminder:
- In the content put "about" followed by the reminder the user wants.
- If date is not specified by the user put "" in the date field.

If the user wants to set a reminder:
- Always generate a natural and specific reminder

If the message continues from a previous one:
- infer the full intent using that context if possible.
- use the action of the previous if the user gives vague or no action for the current one

"""

TOOL_SCHEMA = {
        "parameters": {
            "type": "object",
            "properties": {
                "Content": "Reminder details",
                "Date": "DD-MM-YYYY",
                "Time": "HH:MM",
                "Action": "set/ update/ get/ cancel"
            },
            "required": ["Content", "Date", "Time", "Action"]
        }
}

TOOL_SCHEMA_COMPLETE = {
    "name": "Reminder",
        "description": "Set, update or get reminders for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "Content": "Reminder content",
                "Date": "Reminder date in DD-MM-YYYY format, e.g. 'July 5, 2025' is 05-07-2025 , 'February this year' is 00-02-2025, 'next year' is 00-00-2025 ",
                "Time": "Reminder time in HH:MM format, if no time is given just return '00:00' if 'later' then add 2 hours to the current time ",
                "Unspecified_time": "A fallback to when the user did not specify a time, e.g., 'later' ",
                "Action": {
                    "type": "string",
                    "description": "Choose if the user want to set, update or get a reminder, use the exact string form the enum",
                    "enum": ["set", "update", "get", "cancel"]
                }
            },
            "required": ["Content", "Date", "Time", "Action"]
        }
}