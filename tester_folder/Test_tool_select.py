from agent.vector_helper import search_tool, build_contextual_query
from agent.json_helper import load_conversations_json

##print the last item in the json
last_item = load_conversations_json()[-1]
print(last_item["user"])

text = input("Enter text: ")
prompt = build_contextual_query(text, last_item)
print(search_tool(prompt))