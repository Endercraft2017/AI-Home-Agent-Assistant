from datetime import datetime
import json

tools = [
    {"name": "query",
        "description": "Returns answers to the user's query using own memory and database, i.e when the user asks for things if the agent remember them, 'what did I do yesterday', 'do you remember what my lunch yesterday was', 'did I take vitamins yesterday', and others",
        "parameters": {
            "type": "object",
            "properties": {
                "Query": "The user's query",
            },
            "required": ["Query"]
        }
    },
    {"name": "search",
        "description": "Returns answers and search results that the user asks to search from the internet",
        "parameters": {
            "type": "object",
            "properties": {
                "query": "The user's query",
            },
            "required": ["query"]
        }
    },
    {"name": "get_weather",
        "description": "Returns current weather forcast for the user's location",
        "parameters": {
            "type": "object",
            "properties": {
                "Location": "The user's desired location of the forcast"
                #get the agent's current location and use it as default when the user 
                #did not specify the location
            },
            "required": ["Location"]
        }
    },
    {"name": "Reminder",
        "description": "Set, update or get reminders for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "Content": "Reminder content",
                "Date": "Reminder date in DD:MM:YYYY format",
                "Time": "Reminder time in HH:MM format",
                "Unspecified_time": "A fallback to when the user did not specify a time, e.g., 'later' ",
                "Action": {
                    "type": "string",
                    "description": "Choose if the user want to set, update or get a reminder",
                    "enum": ["set", "update", "get"]
                }
            },
            "required": ["Content","Date", "Time", "Action"]
        }
    },
    {"name": "Note",
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
    },
    {"name": "music",
        "description": "Play or pause music for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "Title": "When the user specify a title",
                "Genre": "When the user specify a genre",
                "Artist": "When the user specify the artist/band",
                "Playlist": "When the user specify the playlist",
                "Action": {
                    "type": "string",
                    "description": "Choose if the user wants to play or pause the music",
                    "enum": ["play", "pause"]
                }
            },
            "required": ["Title","Action"]
        }
    },
    {"name": "microcontroller",
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
    },
    {"name": "chat",
        "description": "A fallback for when user want to have a general conversation, asking for a joke, simple arithmetic and math and logic and reasoning, greetings, suggestions, and others",
        "parameters": {
            "type": "object",
            "properties": {
                "message": "the user's message"
            },
            "required": ["message"]
        }
    },
    
    # …add more tools here…
]