# voice.py
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

MODEL = whisper.load_model("base")

# 🔴 CHANGE THIS to your actual mic index
MIC_DEVICE_INDEX = 2  # e.g. 1

def listen(seconds=6):
    print("🎤 Listening...")
    fs = 16000

    recording = sd.rec(
        int(seconds * fs),
        samplerate=fs,
        channels=1,
        dtype=np.int16,
        device=MIC_DEVICE_INDEX  # 👈 forces correct mic
    )
    sd.wait()
    print("🛑 Recording complete.")

    filename = "voice_input.wav"
    wav.write(filename, fs, recording)

    result = MODEL.transcribe(filename)
    text = result.get("text", "").strip()

    # 🔍 DEBUG OUTPUT
    print(f"[DEBUG] Transcribed text: '{text}'")

    return text
