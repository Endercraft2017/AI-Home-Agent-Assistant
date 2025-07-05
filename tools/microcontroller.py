def run(params):
    device = params.get("Device","lights")
    action = params.get("Action","get")

    ##Run controller code here

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
    "name": "microcontroller",
        "description": "For controlling external devices and getting states of them i.e, esp32, lights, outlets, fans, temperature",
        "parameters": {
            "type": "object",
            "properties": {
                "Device": "The device the user wants to control",
                "Action": {
                    "type": "string",
                    "description": "Choose if the user wants to turn on||off|get the status of the device",
                    "enum": ["on", "off","get"]
                }
            },
            "required": ["Device","Action"]
        }
}