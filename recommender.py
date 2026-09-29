def score_property(p, city, area, property_type, bhk, max_price):

    score = 0

    if city and p["city"].lower() == city.lower():
        score += 30

    if area and p["area"].lower() == area.lower():
        score += 40

    if property_type and p["type"].lower() == property_type.lower():
        score += 30

    if bhk and p["bhk"].lower() == bhk.lower():
        score += 20

    if max_price and p["price"] <= max_price:
        score += 30

    return score


def recommend(properties, city, area, property_type, bhk, max_price):

    if not properties:
        return None

    ranked = sorted(
        properties,
        key=lambda p: score_property(
            p,
            city,
            area,
            property_type,
            bhk,
            max_price
        ),
        reverse=True
    )

    return ranked[0]