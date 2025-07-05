import requests
import json
import os

from instructions import tools

JSON_MEMORY_FILE = "conversation_memory.json"
TEXT_MEMORY_FILE = "conversation.txt"
MAX_JSON = 5

def save_conversation_json(user_text, response_text, memory_file=JSON_MEMORY_FILE, text_file=TEXT_MEMORY_FILE, max_json=MAX_JSON):
    # Load existing data or start new list
    if os.path.exists(memory_file):
        with open(memory_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append new conversation
    data.append({"user": user_text, "response": response_text})

    # If more than max_json, move the oldest to text file and shift
    while len(data) > max_json:
        oldest = data.pop(0)
        with open(text_file, "a", encoding="utf-8") as f:
            f.write(f'User: "{oldest["user"]}"\nResponse: "{oldest["response"]}"\n')

    # Save back to JSON file
    with open(memory_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_conversations_json(memory_file=JSON_MEMORY_FILE):
    if not os.path.exists(memory_file):
        return []
    with open(memory_file, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def build_messages(context, question, prompt_content):
    messages = [{"role": "System", "content": prompt_content}]
    for pair in context:
        messages.append({"role": "user", "content": pair["user"]})
        messages.append({"role": "Assistant", "content": pair["response"]})
    messages.append({"role": "user", "content": question})
    return messages

def SummarizeText(text, model="gemma3:4b"):
    instruction = (
        "You are a text summarization AI. "
        "Do not include any additional information or explanations. "
        "Do not include any emoji in your reply: "
        "Make it short in a way that only the main point remains."
        "Reply only with the summary of this text: \n"
        f"{text}"
    )
    data = {
        "model": model,
        "prompt": instruction,
        "stream": False,
        "temperature": 0.2
    }
    pc_url = "http://192.168.1.131:11434/api/generate"
    url = "http://127.0.0.1:11434/api/generate"
    response = requests.post(pc_url, json=data)
    try:
        response_data = json.loads(response.text)
        response = response_data.get("response", text)
        return response
    except Exception:
        return text

def AI_assistant_chat(question, model="gemma3:4b"):
    prompt_content = (
        "You are an AI Home Assistant.\n"
        "You are designed to assist users with their questions and tasks by providing helpful and accurate responses.\n"
        "Reply using in paragraphs rather than bullet, structure your response in natural language as if you are talking with a mouth.\n"
        "Unless the user want it to be long or specified a word count, Make your replies short and concise, offer additional info if there is too much.\n"
    )
    context = load_conversations_json()
    messages = build_messages(context, question, prompt_content)
    data = {
        "model": model,
        "messages": messages,
        "stream": True,
        "temperature": 0.8,
        "Tools": tools
    }
    pc_url = "http://192.168.1.131:11434/api/chat"
    url = "http://127.0.0.1:11434/api/chat"
    response = requests.post(pc_url, json=data, stream = True)
    reply = ""
    try:
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode("utf-8"))
                    # For Ollama, streamed chunks usually have this structure:
                    last_chunk = chunk
                    content = chunk.get("message", {}).get("content")
                    if content:
                        print(content, end="", flush=True)  # Print as it streams
                        reply += content
                except Exception:
                    continue
        print("\n\n\n")
        if last_chunk:
            print(last_chunk.get("prompt_eval_count"))
            print((last_chunk.get("prompt_eval_duration") or 0) / 1000000000)
            print(last_chunk.get("eval_count"))
            print((last_chunk.get("eval_duration") or 0) / 1000000000)
        print("\n\n\n")
        return reply if reply else "No reply found."
    except Exception:
        return "No reply found."
    

if __name__ == "__main__":
    question = input("Question: ")
    ai_reply = AI_assistant_chat(question, "gemma3")
    #add a "thinking" effect when AI is not yet responding
    #print("AI Reply:", ai_reply, "\n")
    #summarized_reply = SummarizeText(ai_reply, "gemma3:1b")
    #save_conversation_json(question, summarized_reply)
    #print("Summarized AI Reply:", summarized_reply, "\n")