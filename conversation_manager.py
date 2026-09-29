conversation = {
    "name": None,
    "phone": None,
    "budget": None,
    "property": None,
    "city": None
}

def set_value(key, value):
    conversation[key] = value

def get_value(key):
    return conversation.get(key)

def reset():
    global conversation
    conversation = {
        "name": None,
        "phone": None,
        "budget": None,
        "property": None,
        "city": None
    }