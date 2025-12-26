# voice.py
# Voice input + output for JARVIS (Windows-native, stable)

import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import win32com.client

MODEL = whisper.load_model("base")

MIC_DEVICE_INDEX = 2  # keep your working mic index


def listen(seconds=5):
    print("🎤 Listening...")
    fs = 16000

    recording = sd.rec(
        int(seconds * fs),
        samplerate=fs,
        channels=1,
        dtype=np.int16,
        device=MIC_DEVICE_INDEX
    )
    sd.wait()
    print("🛑 Recording complete.")

    filename = "voice_input.wav"
    wav.write(filename, fs, recording)

    result = MODEL.transcribe(filename)
    return result.get("text", "").strip()


def speak(text: str):
    if not text:
        return

    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)
