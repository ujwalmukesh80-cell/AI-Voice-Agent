import json
import os


LEAD_FILE = "leads.json"


def save_lead(name, phone, requirement):

    lead = {
        "name": name,
        "phone": phone,
        "requirement": requirement
    }

    leads = []

    if os.path.exists(LEAD_FILE):

        with open(LEAD_FILE, "r") as f:
            try:
                leads = json.load(f)
            except:
                leads = []

    leads.append(lead)

    with open(LEAD_FILE, "w") as f:
        json.dump(leads, f, indent=4)

    print("Lead Saved.")