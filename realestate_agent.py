from property_search import search_properties
from nlp_parser import extract_filters
from memory import save_properties
from recommender import recommend


def handle_realestate(user):

    # Extract filters from the user's query
    city, area, property_type, bhk, max_price = extract_filters(user)

    # Search matching properties
    properties = search_properties(
        city=city,
        area=area,
        property_type=property_type,
        bhk=bhk,
        max_price=max_price
    )

    if not properties:
        return None

    # Save properties for follow-up questions
    save_properties(properties)

    # Get the best recommended property
    best = recommend(
        properties,
        city,
        area,
        property_type,
        bhk,
        max_price
    )

    if not best:
        return None

    # Build the reply
    reply = f"""
I recommend this property.

🏠 Type: {best['type']}
📍 Location: {best['area']}, {best['city']}
🛏️ BHK: {best['bhk']}
💰 Price: ₹{best['price']:,}
🏢 Builder: {best.get('builder', 'N/A')}
🚗 Parking: {best.get('parking', 'N/A')}

Amenities:
"""

    amenities = best.get("amenities", [])

    if amenities:
        for item in amenities:
            reply += f"\n• {item}"
    else:
        reply += "\n• No amenities listed"

    reply += "\n\nWould you like to schedule a site visit?"

    return reply