import sys
from agent.llm import detect_intent, generate_response, parse_params
from agent.json_helper import load_conversations_json, save_conversation_json, format_conversation_history
from tools import ALL_TOOLS
from agent.sqlite_helper import init_db
from agent.vector_helper import search_tool, build_tool_index, build_contextual_query
#from agent.states import is_waiting, get_pending_tool, clear_followup

if "--rebuild" in sys.argv:
    print("🔄 Rebuilding tool vector index...")
    build_tool_index()
    print("✅ Rebuild complete.")
    exit()

init_db()

def rebuild_tool_index():
    from agent.vector_helper import build_index
    build_index()
    print("Tool index rebuilt.")

def run_agent(user_input):

    #     # Check if the assistant is waiting for a follow-up confirmation
    # if is_waiting():
    #     yes = user_input.lower().strip() in ("yes", "sure", "okay", "yep", "go ahead", "do it", "yup")
    #     no = user_input.lower().strip() in ("no", "not now", "maybe later", "not right now", "nope", "no way")

    #     tool_name, params, followup_type = get_pending_tool()

    #     if yes:
    #         tool_result = ALL_TOOLS[tool_name].run(params)
    #         response = generate_response(user_input, tool_result)
    #         save_conversation_json(user_input, response, tool_name)
    #         clear_followup()
    #         return response
    #     elif no:
    #         clear_followup()
    #         response = "Okay, no changes were made."
    #         save_conversation_json(user_input, response, "NONE")
    #         return response
    #     else:
    #         clear_followup()

    conversations = load_conversations_json()
    context_block = format_conversation_history(conversations)
    context_block_for_response = format_conversation_history(conversations, 3)
    intent = detect_intent(user_input, context_block)
    print(f"[INTENT DETECTED] main.py: {intent}")

    if intent == "tool":
        last_item = conversations[-1]
        prompt = build_contextual_query(user_input, last_item)
        print(f"[PROMPT] main.py: {prompt}")
        tool_use = search_tool(prompt)
        print(f"[TOOLS USED] main.py: {tool_use}")

        return

        params = parse_params(prompt, ALL_TOOLS[tool_use])
        if "error" in params:
            print(f"[ERROR] main.py: {params['error']}")
            return "Sorry, I couldn't understand what you meant."
        print (f"[PARAMS] main.py: {params}")
        
        tool_result = ALL_TOOLS[tool_use].run(params)
        print(f"[TOOL RESULT] main.py: {tool_result}")

        response = generate_response(prompt, tool_result)
        save_conversation_json(user_input, response, tool_use)
        return response

    return

    if intent == "tool":
        # You can later use vector search here
        selected_tool_name = search_tool(user_input)
        tool_module = ALL_TOOLS[selected_tool_name]

        params = parse_params(user_input, tool_module)
        if "error" in params:
            return "Sorry, I couldn't understand what you meant."

        tool_result = tool_module.run(params)
        response = generate_response(user_input, tool_result)
        return response

    elif intent == "chat":
        return generate_response(user_input)
    
    elif intent == "malicious":
        ##add instructions for this in instreuctions.py
        return generate_response(user_input)

    else:
        return "Sorry, I can't handle that request."

# Test
if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")
        reply = run_agent(user_input)
        print("Assistant:", reply)
