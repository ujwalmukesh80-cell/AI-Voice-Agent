import property_db


def get_response(message):

    message = message.lower()

    properties = property_db.get_all_properties()

    results = []

    for p in properties:

        if (
            p["city"].lower() in message
            or p["type"].lower() in message
            or p["bhk"].lower() in message
        ):
            results.append(p)

    if not results:
        return "Sorry, I couldn't find any matching properties."

    reply = "I found these properties:\n\n"

    for p in results:

        reply += (
            f"{p['type']} | "
            f"{p['city']} | "
            f"{p['bhk']} BHK | "
            f"₹{p['price']}\n"
        )

    return reply