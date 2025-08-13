def run(params):
    query = params.get("Query")

    ##Run query code here

    ##Return result

TOOL_LONG_DESCRIPTION = """
A tool for answering the user's personal or past-related questions using the assistant's memory or database.

Use this tool whenever the user asks about something the assistant might have remembered, stored, or been told previously. This includes questions about past actions, previous reminders, stored notes, or any information the assistant might have logged before.

Example use cases:

User: What did I eat for lunch yesterday?  
User: Do you remember what I did on June 12?  
User: What was my last reminder about?  
User: Did I take my vitamins this morning?  
User: Can you recall if I went to the gym yesterday?  
User: What did I ask you to do earlier?  
User: Do you remember my favorite restaurant?  
User: What were we talking about yesterday?  
User: What was my last search?

Use this tool when the user wants to recall previously known or saved information. The assistant will attempt to retrieve this from memory and respond accordingly.
"""
ADDITIONAL_INSTRUCTION = """
Specify the user's query in the `Query` parameter
"""

TOOL_SCHEMA = {
    "parameters": {
        "type": "object",
        "properties": {
            "Query": "The user's query",
        },
        "required": ["Query"]
    }
}

TOOL_SCHEMA_COMPLETE = {
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