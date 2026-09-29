from recorder import record_audio
from transcriber import transcribe_audio

record_audio()

text = transcribe_audio()

print("\nRecognized text:")
print(text)