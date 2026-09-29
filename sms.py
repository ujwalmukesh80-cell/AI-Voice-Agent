from twilio.rest import Client

ACCOUNT_SID = "YOUR_ACCOUNT_SID"
AUTH_TOKEN = "YOUR_AUTH_TOKEN"
TWILIO_NUMBER = "YOUR_TWILIO_WHATSAPP_OR_SMS_NUMBER"

WEBSITE = "https://yourwebsite.com"

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_confirmation(name, phone, property_name, date, time):

    message = f"""
Hello {name},

✅ Your site visit is confirmed.

🏠 Property: {property_name}

📅 Date: {date}

🕙 Time: {time}

You can view the property here:

{WEBSITE}

Thank you for choosing Dream Homes.
"""

    client.messages.create(
        body=message,
        from_=TWILIO_NUMBER,
        to="+91" + phone
    )