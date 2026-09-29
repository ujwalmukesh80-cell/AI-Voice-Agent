import os
from groq import Groq
from dotenv import load_dotenv

from ai.prompt import SYSTEM_PROMPT
from ai.memory import add_message
from ai.memory import get_messages

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_ai(user_message):

    add_message("user", user_message)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(get_messages())

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    reply = response.choices[0].message.content

    add_message("assistant", reply)

    return reply