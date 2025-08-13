from llama_cpp import Llama
import time

MODEL_PATH = "models/gemma-3-4b-it.Q4_K_M.gguf"

# Classification instructions (prepended as a user message)
classification_instructions = """You are a classifier. Your job is to evaluate the user's response in context and label it with:

1. [Yes] or [No] — Is this a follow-up or direct answer to the assistant's previous message?
2. [Chat], [Tool], or [Malicious] — What is the user's intent?

Rules:
- If it's a followup response to the assistant's last message, mark [Yes].
- If it's casual or small talk, mark [Chat].
- If it's a command or utility request, mark [Tool].
- If it's harmful, illegal, or unsafe, mark [Malicious].

Only respond using this format:
[Yes|No] [Chat|Tool|Malicious] [Optional short reply if Chat]

Example:

Assistant: "I've set your reminder for 8:00 AM. Would you like me to set another one?"
User: Yes please

Output:
[Yes] [Chat] Sure, what time?"""

# Turn history for chat mode with proper roles
classification_turns = [
    {
        "role": "assistant",
        "content": "I've set your reminder for 8:00 AM. Would you like me to set another one?"
    },
    {
        "role": "user",
        "content": classification_instructions + '\n\nUser: hi\n\nOutput:'
    }
]
classification_turns_user = [
    {
        "role": "assistant",
        "content": "I've set your reminder for 8:00 AM. Would you like me to set another one?"
    },
    {
        "role": "user",
        "content": classification_instructions + '\n\nUser: can you tell me a joke\n\nOutput:'
    }
]

# Cache of models
_loaded_models = {}

def get_llm_cpp(model_path, instance_name):
    if instance_name not in _loaded_models:
        _loaded_models[instance_name] = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=5,
            n_batch=512,
            use_mmap=True,
            use_mlock=True,
            low_vram=False,
            embedding=False,
            n_gpu_layers=0,
            chat_format="gemma"
        )
    return _loaded_models[instance_name]

def call_llm(prompt=None, messages=None, max_tokens=256, use="response"):
    model = get_llm_cpp(MODEL_PATH, instance_name=use)

    if messages:
        output = model.create_chat_completion(
            messages=messages,
            temperature=0.9,
            max_tokens=max_tokens,
            stop=["</s>"]
        )
        return output["choices"][0]["message"]["content"].strip()
    else:
        output = model(prompt=prompt, max_tokens=max_tokens, temperature=1, stop=["</s>"])
        return output["choices"][0]["text"].strip()

# Loop to evaluate twice using different instruction formats
while True:
    flat_prompt = classification_instructions + "\n\nAssistant: I've set your reminder for 8:00 AM. Would you like me to set another one?\nUser: hi\n\nOutput:"
    flat_prompt2 = classification_instructions + "\n\nAssistant: I've set your reminder for 8:00 AM. Would you like me to set another one?\nUser: can you tell me a joke, dont say jokes about why scientist dont trust atoms, you decide on the joke.\n\nOutput:"

    input("Press enter to continue...")
    call_llm(prompt=flat_prompt, max_tokens=1, use="response")
    #call_llm(prompt="Hello", max_tokens=1, use="intent")
    input("Press enter to continue...")
    print("\n[===llama_cpp Run #1 (chat with correct roles)===")
    start = time.time()
    response = call_llm(prompt=flat_prompt2, max_tokens=20, use="response")
    end = time.time()
    time1 = f"[Eval time] {end - start:.2f}s"
    print(time1)
    print("[Response]", response)

    # Optional: dummy intent ping
    # call_llm(prompt="Hello", max_tokens=1, use="intent")

    # print("\n[===llama_cpp Run #2 (instructions as flat text)===")
    # # Now we test a plain prompt version
    # start = time.time()
    # response = call_llm(messages=classification_turns, max_tokens=20, use="response")
    # end = time.time()
    # print(time1)
    # print(f"[Eval time2] {end - start:.2f}s")
    # print("[Response]", response)

    print(f"\n\nLoaded models: {_loaded_models.keys()}")

    #[Eval time] 20.05s     flat prompt
    #[Eval time2] 4.04s     messages

    #[Eval time] 9.11s      messages
    #[Eval time2] 15.22s    flat prompt

    #[Eval time] 19.80s     flat prompt 
    #[Eval time2] 2.89s     flat prompt cached

    #[Eval time] 8.91s      messages
    #[Eval time2] 2.30s     messages cached

    #[Eval time] 19.43s     messages but combined system and user
    #[Eval time2] 1.53s     messages but combined system and user cached

    #messages is better than flat prompt, try changing the instructions

    #[Eval time] 3.81s (messages cached instructions)
    #[Response] [No] [Chat] Okay, here’s one: Why don’t scientists trust atoms

    #[Eval time] 3.28s (flat prompt cached instructions)
    #[Response] [Yes] [Chat] Sure, here's one: Why don't scientists trust

    #[Eval time] 3.99s (flat prompt cached instructions)(Q6)
    #[Response] [Yes] [Chat] Sure, here’s one: Why don’t scientists trust

    #[Eval time] 3.61s (flat prompt cached instructions)(Q6)
    #[Response] [Yes] [Chat] Sure, here’s one: Why don’t scientists trust

    #conclusion:
    #flat prompt could be used as long as instructions are cached first


