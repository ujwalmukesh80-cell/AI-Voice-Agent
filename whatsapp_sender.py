from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

def send_whatsapp(phone, message):

    client.messages.create(
        from_="whatsapp:+14155238886",
        to=f"whatsapp:{phone}",
        body=message
    )

    print("✅ WhatsApp sent successfully!")