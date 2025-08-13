def run(params):
    device = params.get("Device","lights")
    action = params.get("Action","get")

    ##Run controller code here

    ##Return result

TOOL_LONG_DESCRIPTION ="""
A tool to control smart devices (like ESP32-connected appliances) or retrieve their current status.

Use this tool whenever the user wants to turn a device on or off, or ask for its current status. Devices could include smart lights, fans, outlets, or other appliances connected to a microcontroller (e.g. ESP32).

Example use cases:

User: Turn on the kitchen light  
User: Switch off the bedroom fan  
User: Can you power on the living room outlet?  
User: What's the status of the garage light?  
User: Is the hallway fan running?  
User: I want to check if the dining light is turned off  
User: Turn off everything in the living room  
User: Are the lights still on in the kitchen?
User: Can you get the temperature in the bedroom?
"""

ADDITIONAL_INSTRUCTION = """
Use the full device name (e.g. 'kitchen light', 'ceiling fan', 'thermometer').

Set "Action":
- "on" → turn on the device
- "off" → turn off the device
- "get" → if the user asks for status or reading
"""

TOOL_SCHEMA = {
        "parameters": {
            "type": "object",
            "properties": {
                "Device": "The device the user wants to control",
                "Action": "on/off/get"
            },
            "required": ["Device","Action"]
        }
}

TOOL_SCHEMA_COMPLETE = {
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