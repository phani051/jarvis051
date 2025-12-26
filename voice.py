# voice.py
# OS-independent Voice input + output for JARVIS

import platform
import warnings
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import pyttsx3

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

MODEL = whisper.load_model("base", device="cpu")

MIC_DEVICE_INDEX = 2  # your working mic index
VOICE_INDEX = 1       # 👈 CHANGE THIS (from Step 1)


def listen(silence_timeout=3, samplerate=16000):
    """
    Listen until the user stops speaking.
    Recording stops after `silence_timeout` seconds of silence.
    """
    print("🎤 Listening...")

    frames = []
    silence_duration = 0
    block_duration = 0.1  # seconds per audio block
    silence_threshold = 500  # adjust if needed

    def callback(indata, frames_count, time_info, status):
        nonlocal silence_duration
        volume = np.abs(indata).mean()

        if volume > silence_threshold:
            silence_duration = 0
        else:
            silence_duration += block_duration

        frames.append(indata.copy())

    with sd.InputStream(
        samplerate=samplerate,
        channels=1,
        dtype="int16",
        callback=callback,
        device=MIC_DEVICE_INDEX,
        blocksize=int(samplerate * block_duration)
    ):
        while silence_duration < silence_timeout:
            sd.sleep(int(block_duration * 1000))

    print("🛑 Recording complete.")

    audio = np.concatenate(frames, axis=0)
    filename = "voice_input.wav"
    wav.write(filename, samplerate, audio)

    result = MODEL.transcribe(filename)
    return result.get("text", "").strip()



def speak(text: str):
    if not text:
        return

    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

    # 🔊 Select voice safely
    if 0 <= VOICE_INDEX < len(voices):
        engine.setProperty("voice", voices[VOICE_INDEX].id)

    # Optional tuning
    system = platform.system().lower()
    engine.setProperty("rate", 170 if system == "windows" else 160)
    engine.setProperty("volume", 1.0)

    engine.say(text)
    engine.runAndWait()
    engine.stop()
