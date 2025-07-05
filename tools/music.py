def run(params):
    title = params.get("Title")
    genre = params.get("Genre")
    artist = params.get("Artist")
    playlist = params.get("Playlist")
    action = params.get("Action","play")

    ##Run music code here

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
      "name": "music",
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
}