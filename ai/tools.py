from property_db import get_all_properties
from recommender import recommend


def search_property(city, area, property_type, bhk, budget):

    properties = get_all_properties()

    result = recommend(
        properties,
        city,
        area,
        property_type,
        bhk,
        budget
    )

    return result