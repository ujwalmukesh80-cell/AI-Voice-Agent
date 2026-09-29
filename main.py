import os
import asyncio
from dotenv import load_dotenv
from ai.brain import ask_ai
import edge_tts
from email_sender import send_brochure

from recorder import record_audio
from transcriber import transcribe_audio
from realestate_agent import handle_realestate
from followup import handle_followup
from lead_manager import save_lead
from voice_input import listen
from booking_parser import detect_booking
from booking_manager import save_booking
from brochure import generate_brochure
from memory import get_last_property

load_dotenv()



VOICE = "en-US-AriaNeural"


async def speak(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save("response.mp3")
    os.system("start response.mp3")


print("=" * 60)
print("🏠 AI REAL ESTATE VOICE ASSISTANT")
print("=" * 60)
print("Speak naturally.")
print("Say 'exit' to close the assistant.\n")


while True:

    # -----------------------------
    # Record User Voice
    # -----------------------------
    record_audio()

    # -----------------------------
    # Speech → Text
    # -----------------------------
    user = transcribe_audio()

    if not user:
        continue

    print(f"\nYou: {user}")

    # -----------------------------
    # Exit
    # -----------------------------
    if user.lower() == "exit":
        asyncio.run(speak("Goodbye. Have a wonderful day."))
        print("Goodbye!")
        break

    property_reply = None
    reply = None

        # -----------------------------
    # Generate Brochure
    # -----------------------------
    if "brochure" in user.lower():

        property_data = get_last_property()

        if property_data is None:

            reply = "Please search for a property first."

            print("\nAI:", reply)
            asyncio.run(speak(reply))
            continue

        pdf = generate_brochure(property_data)

        reply = "The brochure has been generated successfully."

        print("\nAI:", reply)
        asyncio.run(speak(reply))

        asyncio.run(
            speak("Would you like me to email the brochure to you?")
        )

        answer = listen()

        if answer and "yes" in answer.lower():

            asyncio.run(
                speak("Please tell me your email address.")
            )

            email = listen()

            send_email(
                email,
                pdf
            )

            asyncio.run(
                speak("Your brochure has been emailed successfully.")
            )

        else:

            asyncio.run(
                speak("No problem.")
            )

        continue

    # -----------------------------
    # Booking Detection
    # -----------------------------
    if detect_booking(user):

        property_data = get_last_property()

        if property_data is None:

            reply = "Please search for a property first."

            print("\nAI:", reply)
            asyncio.run(speak(reply))

            continue

        asyncio.run(speak("Please tell me your name."))
        name = listen()

        asyncio.run(speak("Please tell me your phone number."))
        phone = listen()

        asyncio.run(speak("Which day would you like to visit?"))
        date = listen()

        asyncio.run(speak("What time would you like to visit?"))
        time = listen()

        property_name = (
            f"{property_data['type']} in "
            f"{property_data['area']}"
        )

        save_booking(
            name,
            phone,
            property_name,
            date,
            time
        )

        reply = (
            f"Thank you {name}. "
            f"Your site visit for "
            f"{property_name} "
            f"has been booked on "
            f"{date} at {time}."
        )

        print("\nAI:", reply)
        asyncio.run(speak(reply))

        continue
    # -----------------------------
    # Follow-up Questions
    # -----------------------------
    followup_reply = handle_followup(user)

    if followup_reply:

        reply = followup_reply

    else:

        # -----------------------------
        # Search Property Database
        # -----------------------------
        property_reply = handle_realestate(user)

        if property_reply:

            reply = property_reply

        else:

                       # -----------------------------
            # General AI Conversation
            # -----------------------------
            try:
                reply = ask_ai(user)

            except Exception as e:
                print("Error:", e)
                reply = "Sorry, I couldn't contact the AI server."

    # -----------------------------
    # Speak Response
    # -----------------------------
    print("\nAI:", reply)

    asyncio.run(
        speak(reply)
    )

    # -----------------------------
    # Lead Collection
    # -----------------------------
    if property_reply:

        asyncio.run(
            speak(
                "Would you like to register your interest in this property?"
            )
        )

        print("\nAI: Would you like to register your interest?")

        answer = listen()

        if answer and "yes" in answer.lower():

            asyncio.run(
                speak(
                    "Please tell me your full name."
                )
            )

            print("\nListening for name...")

            name = listen()

            asyncio.run(
                speak(
                    "Please tell me your phone number digit by digit."
                )
            )

            print("\nListening for phone number...")

            phone = listen()

            save_lead(
                name,
                phone,
                user
            )

            print("\n✅ Lead Saved Successfully!")

            asyncio.run(
                speak(
                    f"Thank you {name}. "
                    "Your details have been saved successfully. "
                    "Our sales team will contact you soon."
                )
            )

        else:

            asyncio.run(
                speak(
                    "No problem. Let me know if you need any more help."
                )
            )