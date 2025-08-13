from agent.llm import call_llm
from agent.instructions import PROMPT_TEMPLATES
from datetime import datetime

now = datetime.now()
formatted_datetime = now.strftime("%A, %B %d, %Y, %H:%M")

tool_list = """
'microcontroller' : 'For controlling external devices and getting states of them i.e, esp32, lights, outlets, fans, temperature',
'music' : 'Use this tool whenever the user wants to listen to music, stop it temporarily, or resume playback. The user might specify a song name, a music genre, an artist/band, or a playlist',
'note' : 'Use this tool when the user wants to jot something down, recall what they've previously written, or modify the contents of an existing note.',
'query' : 'Use this tool whenever the user asks about something the assistant might have remembered, stored, or been told previously. This includes questions about past actions, previous reminders, stored notes, or any information the assistant might have logged before.',
'reminder' : 'Use this tool whenever the user asks to create a new reminder, modify an existing one, check for upcoming reminders, or cancel a scheduled reminder.',
'search' : 'Use this tool when the assistant is expected to look up real-time or factual information from the internet, knowledge that isn't stored locally or remembered.',
'weather' : 'Use this tool when the user asks about the weather — including temperature, rain, humidity, or other conditions — either generally or for a specific place.'
"""
def test_tool():
    text = input("Enter text: ")
    prompt = PROMPT_TEMPLATES["tool_selection"].format(user_input=text, tool_list=tool_list, date_time=formatted_datetime)
    print(f"[DEBUG] prompt: \n\n{prompt}")
    response = call_llm(prompt).strip().lower()
    print(response)


YES_NO_INSTRUCTIONS = """
Your task is to Identify if the user's response is an answer or a followup answer from
the assistant's question or statement and also identify the user's intent if the user's
intent is to [Chat] for casual talk or [Tool] to use tools or [Malicious] for malicious requests.

Add a tag [Yes] or [No] to the end of the response if the user's response is an 
answer or a followup answer from the assistant's question or statement.
Add another tag following the [Yes] or [No] tag for the user's intent [Chat], [Tool] or [Malicious]
Analize the Assistant as well, if the user's response is an answer or a followup answer from
the assistant's question or statement then the user's intent must be similar to the assistant's intent.

If the user's intent is a chat ot casual talk then reply to the user input and add [Chat] flag at the start

If the user's intent is a malicious request then reply saying that you do not accept any malicious requests and add [Malicious] tag at the begining

If the user's intent is a tool request then reply with [Tool] flag

Assistant: "I have set your reminder for 8:00 AM, would you like me to set another one?"

User: {user_input}

Output format: [Yes/No] [Chat/Tool/Malicious] [Optional reply if chat]

"""

EXPECTING_FOLLOWUP_INSTRUCTIONS = """
Your task is to Identify if the assistant is expecting a followup response from the user or not.
Answer: "yes" or "no".

Assistant: "I have set your reminder for 8:00 AM, would you like me to set another one?"
"""



def check_yes_no(text):
    call_llm("hello",max_tokens=1)
    prompt1 = YES_NO_INSTRUCTIONS.format(user_input=text)
    #print(f"[DEBUG] prompt: \n\n{prompt1}")
    response = call_llm(prompt1,max_tokens=10).strip().lower()
    #response2 = call_llm(EXPECTING_FOLLOWUP_INSTRUCTIONS).strip().lower()
    print(response)
    #print(response2)

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    check_yes_no(user_input)
