
PROMPT_TEMPLATES = {
    # Step 1: Determine user intent (chat / tool / malicious)
    "intent_detection": """
Classify the user's message into one of the following:

- "chat": Casual talk or simple questions.
- "tool": Requires calling a tool to complete a task.
- "malicious": Unsafe or inappropriate message.

Only return one of: chat, tool, or malicious.

User: "{user_input}"
""",

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
You are an assistant that converts user messages into structured JSON based on a tool schema.

User request: "{user_input}"

Tool schema:
{tool}

Extract only the parameters that match the tool schema. Respond only with a JSON object.
For date and time context, now is: {date_time}

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
