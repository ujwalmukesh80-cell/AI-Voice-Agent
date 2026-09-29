import json

def load_properties():
    with open("properties.json", "r") as file:
        return json.load(file)


def search_property(query):
    properties = load_properties()
    query = query.lower()

    for p in properties:
        if (
            p["city"].lower() in query
            or p["area"].lower() in query
            or p["type"].lower() in query
            or (p["bhk"] and p["bhk"].lower() in query)
        ):
            return p

    return None


def format_property(p):
    return f"""I found a property for you.

Property Type: {p['type']}
City: {p['city']}
Area: {p['area']}
BHK: {p['bhk']}
Price: ₹{p['price']}
Status: {p['status']}

Would you like to schedule a site visit or know more details?"""