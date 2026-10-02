import property_db


def search_property(query, business_id):
    if not business_id:
        return None

    properties = property_db.get_all_properties(business_id)

    query = query.lower()

    for p in properties:

        city = str(p["city"] or "").lower()
        area = str(p["area"] or "").lower()
        property_type = str(p["type"] or "").lower()
        bhk = str(p["bhk"] or "").lower()

        if (
            city in query
            or area in query
            or property_type in query
            or (bhk and bhk in query)
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