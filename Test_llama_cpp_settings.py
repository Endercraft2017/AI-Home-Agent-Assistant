import time
import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "gemma3:4b"  # Change if needed

prompt = """You are a classifier. Your job is to evaluate the user's response in context and label it with:

1. [Yes] or [No] — Is this a follow-up or direct answer to the assistant's previous message?
2. [Chat], [Tool], or [Malicious] — What is the user's intent?

Rules:
- If it's a response to the assistant's last message, mark [Yes].
- If it's casual or small talk, mark [Chat].
- If it's a command or utility request, mark [Tool].
- If it's harmful, illegal, or unsafe, mark [Malicious].

Only respond using this format:
[Yes|No] [Chat|Tool|Malicious] [Optional short reply if Chat]

Example:

Assistant: "I've set your reminder for 8:00 AM. Would you like me to set another one?"
User: Yes please

Output:
[Yes] [Chat] Sure, what time?
"""

prompt2 = """
Your task is to Identify if the user's response is an answer or a followup answer from
the assistant's question or statement and also identify the user's intent if the user's
intent is to [Chat] for casual talk or [Tool] to use tools or [Malicious] for malicious requests.

Add a tag [Yes] or [No] to the end of the response if the user's response is an 
answer or a followup answer from the assistant's question or statement.
Add another tag following the [Yes] or [No] tag for the user's intent [Chat], [Tool] or [Malicious]

Assistant: "I have set your reminder for 8:00 AM, would you like me to set another one?"

User: Yes please

Output format: [Yes/No] [Chat/Tool/Malicious] [Optional reply if chat]
"""

def run_ollama(tag):
    print(f"\n=== {tag} ===")
    if tag == "Ollama Run #1":
        prompts = prompt2
    else:
        prompts = prompt
    start = time.time()
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": prompts,
        "stream": False,
        "options": {
            "num_predict": 64
        }
    })
    end = time.time()
    result = response.json()
    print(f"[Eval time] {end - start:.2f}s")
    print("[Response]", result)

run_ollama("Ollama Run #1")
run_ollama("Ollama Run #2 (cached?)")
