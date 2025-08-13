def run(params):
    title = params.get("Title")
    genre = params.get("Genre")
    artist = params.get("Artist")
    playlist = params.get("Playlist")
    action = params.get("Action","play")

    ##Run music code here

    ##Return result

TOOL_LONG_DESCRIPTION ="""
A tool to play or pause music based on user preferences such as title, genre, artist, or playlist.

Use this tool whenever the user wants to listen to music, stop it temporarily, or resume playback. The user might specify a song name, a music genre, an artist/band, or a playlist.

Example use cases:

User: Play some jazz music  
User: Pause the song  
User: Play "Bohemian Rhapsody"  
User: Can you play my workout playlist?  
User: Start playing BTS songs  
User: Play something by Coldplay  
User: Resume the music  
User: Pause the music for now  
User: I want to listen to chill lo-fi  
User: Play the next song on my driving playlist  
User: Can you stop the music?  
User: Can you turn off the music?
"""

ADDITIONAL_INSTRUCTION = """
Extract all relevant music information the user provides — including title, genre, artist, or playlist — but only fill in fields that are explicitly mentioned.

For "Title", prefer full song titles when possible.  
If the user only says a genre (e.g., "play some jazz"), fill in the Genre field and leave Title blank.  
If the user mentions an artist or band, place that in the Artist field.  
If they mention a playlist (e.g., “my workout mix”), assign it to Playlist.

Always set the "Action" as either "play" or "pause" based on the user's intent.

Avoid vague terms like “some music” in the Title field. If no specific song title is given, leave Title blank and use Genre, Artist, or Playlist as appropriate.
"""

TOOL_SCHEMA = {
      "parameters": {
          "type": "object",
          "properties": {
              "Title": "song title",
              "Genre": "music genre",
              "Artist": "artist/band",
              "Playlist": "music playlist",
              "Action": "play/ pause"
          },
          "required": ["Title/Genre/Artist/Playlist", "Action"]
        }
}

TOOL_SCHEMA_COMPLETE = {
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