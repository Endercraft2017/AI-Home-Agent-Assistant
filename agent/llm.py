# agent/llm.py

import requests
import json
from .instructions import PROMPT_TEMPLATES
from config import OLLAMA_URL, DEFAULT_MODEL, EMBED_MODEL
from datetime import datetime

now = datetime.now()
formatted_datetime = now.strftime("%A, %B %d, %Y, %H:%M")

def call_llm(prompt, model=DEFAULT_MODEL, format="text ", stream=False):
    payload = {
        "model": model,
        "prompt": prompt,
        "format": format,
        "stream": stream,
        "temperature": 0.2
    }
    if model == EMBED_MODEL:
        response = requests.post(f"{OLLAMA_URL}/api/embeddings", json=payload)
        return response
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    return response.json()["response"]

def detect_intent(user_input):
    prompt = PROMPT_TEMPLATES["intent_detection"].format(user_input=user_input)
    return call_llm(prompt).strip().lower()

def select_tools(user_input, tool_list):
    prompt = PROMPT_TEMPLATES["tool_selection"].format(user_input=user_input, tool_list=tool_list, date_time=formatted_datetime)
    return call_llm(prompt).strip().lower()

def parse_tool_params(user_input, tool_schema):
    prompt = PROMPT_TEMPLATES["tool_parse"].format(user_input=user_input, tool=tool_schema, date_time=formatted_datetime)
    return json.loads(call_llm(prompt,DEFAULT_MODEL,"json"))

def embed_text(text:str) -> list:
    try:
        response = call_llm(text,EMBED_MODEL)
        return response.json()["embedding"]
    except Exception as e:
        print(f"[DEBUG] llm.py: {e}")
        return e

def generate_response(user_input, tool_result=None):
    if tool_result:
        prompt = PROMPT_TEMPLATES["tool_response"].format(user_input=user_input, result=tool_result)
    else:
        prompt = PROMPT_TEMPLATES["chat_response"].format(user_input=user_input)
    return call_llm(prompt, format="text")
    #stream the response to the User in parallel with sending it to the llm to be summarized and saved to memory 

def SummarizeText(text, model=DEFAULT_MODEL):
    prompt = PROMPT_TEMPLATES["summary_instruction"].format(text = text)
    return call_llm(prompt,model)

def build_messages(context, question, system_prompt):
    messages = [{"role": "System", "content": system_prompt}]
    for pair in context:
        messages.append({"role": "user", "content": pair["user"]})
        messages.append({"role": "Assistant", "content": pair["response"]})
    messages.append({"role": "user", "content": question})
    return messages

def chat(user_input,context,system_prompt):
    prompt_content = (
        "You are an AI Home Assistant.\n"
        "You are designed to assist users with their questions and tasks by providing helpful and accurate responses.\n"
        "Reply using in paragraphs rather than bullet, structure your response in natural language as if you are talking with a mouth.\n"
        "Unless the user want it to be long or specified a word count, Make your replies short and concise, offer additional info if there is too much.\n"
    )
    messages = build_messages(context, user_input, system_prompt)
    data = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "stream": True,
        "temperature": 0.8,
    }
    response = requests.post(f"{OLLAMA_URL}/api/chat", json=data, stream = True)
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
        # print("\n\n\n")
        # if last_chunk:
        #     print(last_chunk.get("prompt_eval_count"))
        #     print((last_chunk.get("prompt_eval_duration") or 0) / 1000000000)
        #     print(last_chunk.get("eval_count"))
        #     print((last_chunk.get("eval_duration") or 0) / 1000000000)
        # print("\n\n\n")
        return reply if reply else "No reply found."
    except Exception:
        return "No reply found."
    #stream the response to the User in parallel with sending it to the llm to be summarized and saved to memory