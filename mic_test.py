import sounddevice as sd
import numpy as np

DEVICE = 9  # WASAPI microphone

print("Speak into your microphone...\n")

def callback(indata, frames, time, status):
    volume = np.linalg.norm(indata) * 10
    print(f"\rVolume: {volume:.2f}", end="")

with sd.InputStream(device=DEVICE,
                    channels=1,
                    samplerate=48000,
                    callback=callback):
    sd.sleep(10000)  # Listen for 10 seconds

print("\nDone.")