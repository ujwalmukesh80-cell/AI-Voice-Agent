import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

SAMPLE_RATE = 16000
DURATION = 7          # Record for 7 seconds
DEVICE = None         # Default microphone

def record_audio(filename="recording.wav"):
    print("\n🎤 Speak after the beep...")
    print("Recording...")

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=DEVICE
    )

    sd.wait()

    # Increase microphone volume
    audio = audio * 3

    # Prevent clipping
    audio = np.clip(audio, -1, 1)

    audio = (audio * 32767).astype(np.int16)

    write(filename, SAMPLE_RATE, audio)

    print("✅ Recording saved.")