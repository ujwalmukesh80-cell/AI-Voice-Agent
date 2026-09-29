def detect_booking(text):

    text = text.lower()

    keywords = [
        "book",
        "booking",
        "site visit",
        "visit",
        "appointment",
        "schedule"
    ]

    return any(word in text for word in keywords)