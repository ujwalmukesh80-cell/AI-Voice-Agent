import json
import os
from datetime import datetime

FILE = "call_logs.json"

def save_call(name, phone, requirement, property_name):

    call = {
        "name": name,
        "phone": phone,
        "requirement": requirement,
        "property": property_name,
        "time": datetime.now().strftime("%d-%m-%Y %H:%M")
    }

    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []
    else:
        data = []

    data.append(call)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)