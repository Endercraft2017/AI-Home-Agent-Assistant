def run(params):
    query = params.get("Query")

    ##Run query code here

    ##Return result

TOOL_LONG_DESCRIPTION = """
A tool to set a reminder, update a reminder, fetch or get a reminder, and cancel a reminder for the user.
Use this tool when the user want anything to do about reminders.

Example use cases:

User: Add a reminder for going to the dentist tommorow at 3 pm
User: Set a reminder for my dinner later at 7 pm
User: I need a reminder for ...
User: Remind me about my ...
User: Can you cancel my reminder for ...
User: Do I have a reminder set for tommorow?
User: Can you look if I have a reminder for ...
User: I need you to change my reminder for ...
User: can you update my reminder to ...
"""

TOOL_SCHEMA = {
    "name": "query",
        "description": "Returns answers to the user's query using own memory and database, i.e when the user asks for things if the agent remember them, 'what did I do yesterday', 'do you remember what my lunch yesterday was', 'did I take vitamins yesterday', and others",
        "parameters": {
            "type": "object",
            "properties": {
                "Query": "The user's query",
            },
            "required": ["Query"]
        }
}