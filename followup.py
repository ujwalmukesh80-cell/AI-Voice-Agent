from memory import get_last_property


def handle_followup(user):

    p = get_last_property()

    if not p:
        return None

    q = user.lower()

    if "parking" in q:
        return f"Yes. It has {p.get('parking', 'parking information not available')}."

    if "builder" in q:
        return f"The builder is {p.get('builder', 'not available')}."

    if "square" in q or "sqft" in q or "size" in q:
        return f"The property size is {p.get('sqft', 'not available')} square feet."

    if "amenities" in q or "facility" in q or "facilities" in q:

        amenities = p.get("amenities", [])

        if amenities:
            return "It includes " + ", ".join(amenities) + "."

        return "Amenities information is not available."

    if "price" in q:
        return f"The price is ₹{p['price']:,}."

    return None