# agent/llm.py

import requests
import json
import time
import multiprocessing
from llama_cpp import Llama
import os
from .instructions import PROMPT_TEMPLATES
from config import OLLAMA_URL, DEFAULT_MODEL, EMBED_MODEL, LLAMA_CPP_MODEL_DIR
from datetime import datetime

now = datetime.now()
formatted_datetime = now.strftime("%A, %B %d, %Y, %H:%M")

_loaded_models = {}  # Cache for loaded Llama instances

# Helper to load and cache models
def get_llm_cpp(model_name):
    if model_name not in _loaded_models:
        model_path = os.path.join(LLAMA_CPP_MODEL_DIR, model_name)
        print(f"[DEBUG] Loading llama-cpp model: {model_path}")
        if model_name == EMBED_MODEL:
            _loaded_models[model_name] = Llama(
            model_path=model_path,
            embedding=True,  # always enabled, safe for chat or embedding models
            n_ctx=2048,
            n_threads=multiprocessing.cpu_count(),
            use_mmap=True,
            use_mlock=False,
            verbose=False
            )
            return _loaded_models[model_name]
        _loaded_models[model_name] = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_batch=256,
            n_threads=6,
            n_parallel=2,
            use_mmap=False,
            use_mlock=True,
            low_vram=False,
            verbose=False
        )
    return _loaded_models[model_name]

# Drop-in replacement for Ollama version
def call_llm(prompt, model=DEFAULT_MODEL, format="text", stream=False, max_tokens=256, use = "response"):
    llm_intent = get_llm_cpp(model)
    llm_parse = get_llm_cpp(model)
    llm_response = get_llm_cpp(model)
    llm_summary = get_llm_cpp(model)
    llm_tool = get_llm_cpp(model)
    llm_embed = get_llm_cpp(EMBED_MODEL)


    # === Embedding model ===
    if model == EMBED_MODEL:
        start_time = time.time()
        result = llm_embed.create_embedding(prompt)
        duration = time.time() - start_time
        print(f"[DEBUG] Embedding eval time: {duration:.2f}s\n")
        return result["data"][0]["embedding"]

    # === Format prompt if JSON requested ===
    if format == "json":
        prompt = f"Respond in JSON format:\n{prompt}"

    # === Streaming mode ===
    if stream:
        start_time = time.time()
        output = ""
        for chunk in llm_response(prompt = prompt,max_tokens = max_tokens, temperature=0.2, stream=True, suffix=None):
            output += chunk["choices"][0]["text"]
        duration = time.time() - start_time
        print(f"[DEBUG] Llama-cpp stream eval time: {duration:.2f}s\n")
        return output

    # === Normal generation ===
    start_time = time.time()
    if use == "response":
        output = llm_response(prompt = prompt,max_tokens = max_tokens, temperature=0.2, suffix=None)
    elif use == "intent":
        output = llm_intent(prompt = prompt,max_tokens = max_tokens, temperature=0.2, suffix=None)
    elif use == "parse":
        output = llm_parse(prompt = prompt,max_tokens = max_tokens, temperature=0.2, suffix=None)
    elif use == "tool":
        output = llm_tool(prompt = prompt,max_tokens = max_tokens, temperature=0.2, suffix=None)
    elif use == "summary":
        output = llm_summary(prompt = prompt,max_tokens = max_tokens, temperature=0.2, suffix=None)
    duration = time.time() - start_time

    response = output["choices"][0]["text"]
    print(f"[DEBUG] llmp.py Llama-cpp eval time: {duration:.2f}s\n")
    return response

def detect_intent(user_input,context_block):
    prompt = PROMPT_TEMPLATES["intent_detection"].format(user_input=user_input, chat_history=context_block)
    #print(f"[DEBUG] llm.py prmopt: {prompt}")
    return call_llm(prompt = prompt,use="intent").strip().lower()

def select_tools(user_input, tool_list):
    prompt = PROMPT_TEMPLATES["tool_selection"].format(user_input=user_input, tool_list=tool_list, date_time=formatted_datetime)
    return call_llm(prompt = prompt,use="tool").strip().lower()

def parse_params(user_input, tool_module):
    tool_schema = tool_module.TOOL_SCHEMA
    additional_instruction = tool_module.ADDITIONAL_INSTRUCTION
    print(f"[DEBUG] llm.py additional_instruction: {additional_instruction}")
    prompt = PROMPT_TEMPLATES["tool_parse"].format(
        user_input=user_input,
        tool=tool_schema,
        additional_instruction=additional_instruction,
        date_time=formatted_datetime
    )
    try:
        return json.loads(call_llm(prompt = prompt, model = DEFAULT_MODEL,format="json",use="parse"))
    except Exception as e:
        return {"error": str(e)}

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
    return call_llm( prompt = prompt, format="text", use="response")
    #stream the response to the User in parallel with sending it to the llm to be summarized and saved to memory 

def SummarizeText(text, model=DEFAULT_MODEL):
    prompt = PROMPT_TEMPLATES["summary_instruction"].format(text = text)
    return call_llm(prompt = prompt,model = model,use="summary")

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