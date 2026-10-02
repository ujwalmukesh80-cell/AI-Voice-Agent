import json
import os
from datetime import datetime

FILE = "call_logs.json"


def save_call(
    name,
    phone,
    requirement,
    property_name,
    business_id=None
):

    if not business_id:
        raise ValueError("No business ID provided")

    call = {
        "name": name,
        "phone": phone,
        "requirement": requirement,
        "property": property_name,
        "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "business_id": business_id
    }

    if os.path.exists(FILE):

        try:
            with open(FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

        except (json.JSONDecodeError, OSError):
            data = []

    else:
        data = []

    data.append(call)

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return True


def load_calls(business_id=None):

    if not business_id:
        return []

    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    except (json.JSONDecodeError, OSError):
        return []

    return [
        call
        for call in data
        if call.get("business_id") == business_id
    ]