from llama_cpp import Llama
import time

MODEL_PATH = "models/gemma-3-4b-it.Q4_K_M.gguf"

# Full structured classification prompt
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

_loaded_models = {}  # Cache for loaded Llama instances

# Helper to load and cache models
def get_llm_cpp(model_name,instance_name):
    if instance_name not in _loaded_models:
        model_path = MODEL_PATH
        _loaded_models[instance_name] = Llama(
            model_path=MODEL_PATH,
            n_ctx=2048,
            n_threads=5,
            n_batch=512,
            use_mmap=True,
            use_mlock=True,
            low_vram=False,
            embedding=False,
            n_gpu_layers=0,
            chat_format=None
        )
    return _loaded_models[instance_name]

# Drop-in replacement for Ollama version
def call_llm(prompt, model=MODEL_PATH, format="text", stream=False, max_tokens=256, use = "response"):
    llm_intent = get_llm_cpp(model,instance_name="intent")
    llm_response = get_llm_cpp(model, instance_name="response")
    llm_chat = get_llm_cpp(model, instance_name="chat")
    llm_tools = get_llm_cpp(model, instance_name="tools")

    # === Normal generation ===
    if use == "response":
        output = llm_response(prompt = prompt,max_tokens = max_tokens, temperature=0.2, suffix=None, stop=["</s>"])
    elif use == "intent":
        output = llm_intent(prompt = prompt,max_tokens = max_tokens, temperature=0.2, suffix=None, stop=["</s>"])

    response = output["choices"][0]["text"].strip()
    return response

# Evaluate twice to test prompt reuse
while True:
    text =input("Press enter to continue...")
    print(f"\n[===llama_cpp Run #1===]\n")
    start = time.time()
    response = call_llm(prompt = prompt2, max_tokens=10, use = "response")
    end = time.time()
    print(f"[Eval time] {end - start:.2f}s")
    print("[Response]", response)

    call_llm(prompt=text, max_tokens=1,use="intent")

    print(f"\n[===llama_cpp Run #2===]\n")
    start = time.time()
    response = call_llm(prompt = prompt, max_tokens=10, use="response")
    end = time.time()
    print(f"[Eval time] {end - start:.2f}s")
    print("[Response]", response)
    print(f"\n\n\n {_loaded_models}")