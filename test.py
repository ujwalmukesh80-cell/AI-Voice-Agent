import sounddevice as sd

device_id = 9

print("Default devices:", sd.default.device)
print("\nDevice information:")
print(sd.query_devices(device_id))