import json
import os

FILE = "leads.json"

def save_lead(name, phone, requirement):

    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            leads = json.load(f)
    else:
        leads = []

    leads.append({
        "name": name,
        "phone": phone,
        "requirement": requirement
    })

    with open(FILE, "w") as f:
        json.dump(leads, f, indent=4)

    return True