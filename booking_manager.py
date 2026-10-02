import json
import os

BOOKING_FILE = "bookings.json"


def _business_id():
    try:
        from flask import session
        return session.get("business_id")
    except Exception:
        return None


def load_bookings(business_id=None):

    business_id = business_id or _business_id()

    if not business_id:
        return []

    if not os.path.exists(BOOKING_FILE):
        return []

    try:
        with open(BOOKING_FILE, "r", encoding="utf-8") as f:
            bookings = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    return [
        booking
        for booking in bookings
        if booking.get("business_id") == business_id
    ]


def save_booking(
    name,
    phone,
    property_name,
    date,
    time,
    business_id=None
):

    business_id = business_id or _business_id()

    if not business_id:
        raise ValueError("No business ID provided")

    booking = {
        "name": name,
        "phone": phone,
        "property": property_name,
        "date": date,
        "time": time,
        "business_id": business_id
    }

    if os.path.exists(BOOKING_FILE):

        try:
            with open(BOOKING_FILE, "r", encoding="utf-8") as f:
                bookings = json.load(f)

        except (json.JSONDecodeError, OSError):
            bookings = []

    else:
        bookings = []

    bookings.append(booking)

    with open(BOOKING_FILE, "w", encoding="utf-8") as f:
        json.dump(bookings, f, indent=4)

    print("Booking Saved")

    return True