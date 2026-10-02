import lead_db


def save_lead(name, phone, requirement, business_id):

    if not business_id:
        raise ValueError("No business ID provided")

    lead = {
        "name": name,
        "phone": phone,
        "email": "",
        "interested_property": requirement,
        "status": "New"
    }

    lead_db.add_lead(
        lead,
        business_id
    )

    return True