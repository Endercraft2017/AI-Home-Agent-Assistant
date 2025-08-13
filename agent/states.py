state = {
    "awaiting_followup": False,
    "pending_tool": None,
    "pending_params": None,
    "followup_type": None,
}

def set_followup(tool, params, followup_type="confirm"):
    state["awaiting_followup"] = True
    state["pending_tool"] = tool
    state["pending_params"] = params
    state["followup_type"] = followup_type

def clear_followup():
    state["awaiting_followup"] = False
    state["pending_tool"] = None
    state["pending_params"] = None
    state["followup_type"] = None

def is_waiting():
    return state["awaiting_followup"]

def get_pending_tool():
    return state["pending_tool"], state["pending_params"], state["followup_type"]
