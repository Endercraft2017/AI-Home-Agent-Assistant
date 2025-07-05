def run(params):
    query = params.get("Query")

    ##Run search code here

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
    "name": "search",
       "description": "Returns answers and search results that the user asks to search from the internet",
       "parameters": {
           "type": "object",
           "properties": {
               "query": "The user's query",
           },
           "required": ["query"]
       }
}