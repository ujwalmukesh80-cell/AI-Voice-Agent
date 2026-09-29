import json
import os

BOOKING_FILE = "bookings.json"


def save_booking(name, phone, property_name, date, time):

    booking = {
        "name": name,
        "phone": phone,
        "property": property_name,
        "date": date,
        "time": time
    }

    if os.path.exists(BOOKING_FILE):

        with open(BOOKING_FILE, "r") as f:
            try:
                bookings = json.load(f)
            except:
                bookings = []

    else:
        bookings = []

    bookings.append(booking)

    with open(BOOKING_FILE, "w") as f:
        json.dump(bookings, f, indent=4)

    print("✅ Booking Saved")