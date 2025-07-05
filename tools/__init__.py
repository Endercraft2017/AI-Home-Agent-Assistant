from . import weather, music, note, microcontroller, search, query, reminder

ALL_TOOLS = {
    "get_weather": weather,
    "music": music,
    "note": note,
    "control_device": microcontroller,
    "search": search,
    "query": query,
    "reminder": reminder
}

ALL_TOOLS_LONG_DESCRIPTION = {
    "reminder" : reminder.TOOL_LONG_DESCRIPTION 
}