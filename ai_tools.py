from property_db import get_all_properties
from recommender import recommend


def recommend_property(city, area, property_type, bhk, max_price):

    properties = get_all_properties()

    result = recommend(
        properties,
        city,
        area,
        property_type,
        bhk,
        max_price
    )

    if result:

        return (
            f"I found a {result['bhk']} "
            f"{result['type']} in "
            f"{result['area']}, {result['city']} "
            f"for ₹{result['price']}."
        )

    return "Sorry, I couldn't find a matching property."