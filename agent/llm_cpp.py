# DEFAULT_MODEL = "gemma3:4b"
# EMBED_MODEL = "mxbai-embed-large"
# 
# def call_llm(prompt, model=DEFAULT_MODEL, format="text", stream=False):
#     if format == "json":
#         payload = {
#             "model": model,
#             "prompt": prompt,
#             "format": format,
#             "stream": stream,
#             "temperature": 0.2
#         }
#     else:
#         payload = {
#             "model": model,
#             "prompt": prompt,
#             "stream": stream,
#             "temperature": 0.2
#         }
#     if model == EMBED_MODEL:
#         response = requests.post(f"{OLLAMA_URL}/api/embeddings", json=payload)
#         return response
#     response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
#     try:
#         response_json = response.json()
#     except Exception:
#         print(f"[DEBUG] Invalid JSON from Ollama:\n{response.text}")
#         raise
#     if "response" not in response_json:
#         print(f"[DEBUG] Missing 'response' key:\n{json.dumps(response_json, indent=2)}")
#         raise ValueError("LLM did not return a 'response' key")
    
#     print(f"[DEBUG] llm.py Eval time:{response.json()['prompt_eval_duration']/1000000000}\n\n")
#     return response.json()["response"]