
PROMPT_TEMPLATES = {
    # Step 1: Determine user intent (chat / tool / malicious)
    "intent_detection": """
You are a message classifier inside a home assistant.

Your job is to decide the type of the user's latest message, based on the content **and** the recent conversation history.

Note: If the assistant just gave a factual/tool-based response, and the user follows up with a vague or open-ended message like "what about X", classify it as "tool" if X could involve up-to-date information, external lookup, or control actions.

Classify the message below. Respond with only one of: "chat", "tool", or "malicious".

- "tool" → if the message asks about something the assistant can't directly know or recall (like reminders, notes, current time, controlling devices, or searching the web).
- "chat" → if the message continues casual talk, jokes, opinions, or general conversation.
- "malicious" → if the message is unsafe, inappropriate, or suspicious.

Here is the conversation so far:
<Start chat history>
{chat_history}
<End chat history>

Now analyze the following message as a possible continuation:

user: "{user_input}"

Classify it as only one of: "chat", "tool", or "malicious".
"""
,

    # Step 2: Decide which tool to use
    # only pass in the name and description of the tool
    # skip this step if vector db gave only 1 tool
    "tool_selection": """
You are a smart AI home assistant that can use tools.
For context today is: {date_time}
A user asked the following:

"{user_input}"

Here are the available tools:
{tool_list}

Which tool is the most appropriate to use?

Respond with ONLY the tool name (exact string from the list), or "none" if no tool is needed.
""",

    # Step 3: Parse the user input into tool parameters
    "tool_parse": """
You are an assistant that extracts structured JSON tool arguments from user messages based on a tool schema.

User message: "{user_input}"

Tool schema:
{tool}

If the message continues from a previous one, infer the full intent using that context if it is relevant or related. Rewrite vague or short phrases into fully-formed, detailed input as if you were a user.

{additional_instruction}

Current date/time: {date_time}

Return only a JSON object that matches the tool's parameters exactly.

Example format:
{{ "param1": "value1", "param2": "value2" }}
""",

    # Step 4: Respond to the user using the tool result
    "tool_response": """
You are a friendly AI assistant.

User asked:
"{user_input}"

Tool result:
{result}

Now reply to the user in natural language using this result.
Sometimes the tool gives irrelevant or confusing results.
Filter out any irrelevant or confusing results based on the user's query.
If the tool failed:
Reply stating that you are sorry and could not perform the task.
Ask for the user to try again with a more specific query.
""",

    # Fallback/general chat
    "chat_response": """
You are a helpful AI assistant.

User: "{user_input}"

Reply naturally and concisely.
""",

    #Summarize output
    "summary_instruction": """
You are a text summarization AI.
Do not include any additional information or explanations.
Do not include any emoji in your reply:
Make it short in a way that only the main point remains.
Reply only with the summary of this text:

"{text}"

"""
}
