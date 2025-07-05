import sys
from agent.llm import detect_intent, generate_response
from agent.tool_parser import parse_params
from tools import ALL_TOOLS
from agent.sqlite_helper import init_db
from agent.vector_helper import search_tool, build_tool_index

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
    intent = detect_intent(user_input)
    print(f"[INTENT DETECTED]: {intent}")

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

    else:
        return "Sorry, I can't handle that request."

# Test
if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")
        reply = run_agent(user_input)
        print("Assistant:", reply)
