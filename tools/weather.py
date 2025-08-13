def run(params):
    location = params.get("Location","Morong,Rizal")

    ##Run controller code here

    ##Return result

TOOL_LONG_DESCRIPTION = """
A tool to retrieve the current weather forecast based on the user's location.

Use this tool when the user asks about the weather — including temperature, rain, humidity, or other conditions — either generally or for a specific place.

If the user does **not** specify a location, assume they mean their current location (retrieved by the assistant automatically). If they mention a city, region, or country, pass that as the `Location` parameter.

Example use cases:

User: What's the weather like today?  
User: Is it going to rain later?  
User: Can you check the weather in Manila?  
User: What's the temperature outside?  
User: Show me the forecast for tomorrow in Baguio  
User: Do I need an umbrella today?  
User: What's the humidity right now?

Use this tool only for weather-related queries and make sure to pass a valid `Location` string — either specified by the user or defaulted to their current location.
"""

ADDITIONAL_INSTRUCTION = """
Specify the user's location in the `Location` parameter.
If no location is given then use the agents current location as default.
"""

TOOL_SCHEMA = {
    "parameters": {
        "type": "object",
        "properties": {
            "Location": "The user's desired location of the forcast"
            #get the agent's current location and use it as default when the user 
            #did not specify the location
        },
        "required": ["Location"]
    }
}

TOOL_SCHEMA_COMPLETE = {
"name": "get_weather",
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
}