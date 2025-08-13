def run(params):
    query = params.get("Query")

    ##Run search code here

    ##Return result

TOOL_LONG_DESCRIPTION = """
A tool for retrieving up-to-date information from the internet when the user asks about something the assistant cannot answer from memory or local knowledge.

Use this tool whenever the user requests current events, trends, public data, or general knowledge that may change over time or requires browsing the web.

Example use cases:

User: What's the weather today?  
User: Search for the latest iPhone reviews  
User: Can you find popular fashion trends in 2025?  
User: Who won the game last night?  
User: What is the latest news about the stock market?  
User: What are the symptoms of dengue fever?  
User: Search YouTube for relaxing music playlists  
User: What movies are playing in theaters now?  
User: How do I reset my router?

Use this tool when the assistant is expected to look up real-time or factual information that isn't stored locally or remembered.
"""
ADDITIONAL_INSTRUCTION = """
Always generate a complete, natural, and specific query — as if you were searching Google for the user. Include keywords like “current”, “latest”, or the year if it helps clarify the search.

Avoid repetition like “trending trends” or “search on the internet.” Use clear, natural phrases.
"""

TOOL_SCHEMA = {
    "parameters": {
        "type": "object",
        "properties": {
            "query": "The search term or topic the user is asking about"
        },
        "required": ["query"]
    }
}

TOOL_SCHEMA_COMPLETE = {
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