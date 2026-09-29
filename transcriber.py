import whisper

print("Loading Whisper model... (first time takes a minute)")

model = whisper.load_model("base")

def transcribe_audio(filename="recording.wav"):
    result = result = model.transcribe(
    filename,
    language="en",
    fp16=False
)
    return result["text"].strip()