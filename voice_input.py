from recorder import record_audio
from transcriber import transcribe_audio


def listen():

    record_audio()

    text = transcribe_audio()

    if text:
        print("You:", text)
        return text

    return ""