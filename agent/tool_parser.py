from agent.instructions import PROMPT_TEMPLATES
from agent.llm import call_llm
import json

def parse_params(user_input, tool_module):
    tool_schema = tool_module.TOOL_SCHEMA
    prompt = PROMPT_TEMPLATES["tool_parse"].format(
        user_input=user_input,
        tool=tool_schema
    )
    try:
        return json.loads(call_llm(prompt, format="json"))
    except Exception as e:
        return {"error": str(e)}
