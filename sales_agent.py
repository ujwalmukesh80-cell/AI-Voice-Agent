import re

from conversation_manager import get_value, set_value
from intent import detect_budget
from property_search import search_properties


def sales_flow(user):

    text = user.lower()

    # Detect city
    if "hyderabad" in text:
        set_value("city", "Hyderabad")

    # Detect property type
    if "villa" in text:
        set_value("property", "Villa")

    elif "apartment" in text:
        set_value("property", "Apartment")

    elif "plot" in text:
        set_value("property", "Plot")

    # Detect budget
    budget = detect_budget(text)

    if budget:
        set_value("budget", budget)

    # Ask for missing information

    if not get_value("property"):
        return "What type of property are you looking for? Apartment, Villa or Plot?"

    if not get_value("city"):
        return "Which city are you looking in?"

    if not get_value("budget"):
        return "May I know your budget?"

    # Search database

    properties = search_properties(
        city=get_value("city"),
        property_type=get_value("property"),
        max_price=get_value("budget")
    )

    if not properties:
        return "Sorry, I couldn't find a matching property."

    p = properties[0]

    return (
        f"I found a {p['type']} in {p['area']} "
        f"for ₹{p['price']:,}. "
        "Would you like to schedule a site visit?"
    )