# 🤖 JARVIS – Local Voice AI Assistant

JARVIS is a **fully local, offline AI assistant** built using **Ollama**, **Python**, and **qwen3:0.6b**.
It supports **conversation memory**, **voice input**, **voice output**, and a clean **agent-style architecture**
designed for stability on **Windows**.

No cloud APIs. No subscriptions. Full control.

---

## ✨ Features

- 🧠 Local LLM via **Ollama**
- 💬 Conversational continuity (session memory)
- 🗣️ Voice input (Speech → Text) using **Whisper**
- 🔊 Voice output (Text → Speech) using **Windows SAPI**
- 🎤 Continuous voice mode
- ⌨️ Text fallback mode
- 🧾 Explicit memory commands
- 🚪 Voice-based exit with spoken farewell
- 🖥️ Windows-first, offline, CPU-friendly

---

## 🧱 Project Structure

```
JARVIS/
├── jarvis.py          # CLI entry point (agent loop, voice mode, control)
├── brain.py           # LLM interaction (Ollama requests)
├── memory.py          # In-session conversation memory
├── context.py         # System persona & instructions (JARVIS)
├── model_loader.py    # Model readiness & warm-up checks
├── voice.py           # Voice input (STT) and output (TTS)
├── config.py          # Central configuration
└── Modelfile          # Custom Ollama model definition
```

---

## 🧠 Model Used

- **Base model:** qwen3:0.6b
- **Runtime:** Ollama
- **Why this model?**
  - Fast startup
  - Low memory usage
  - Good conversational quality
  - Ideal for local assistants

---

## ⚙️ Requirements

### Software
- Windows 10 / 11
- Python 3.10+
- Ollama installed and running

### Python Packages
```
pip install requests sounddevice numpy scipy openai-whisper pywin32
```

### Ollama
```
ollama pull qwen3:0.6b
```

---

## 🛠️ Setup

### 1️⃣ Create Custom JARVIS Model

Example Modelfile:
```
FROM qwen3:0.6b

SYSTEM """
You are JARVIS, an advanced AI assistant.
Always be concise, professional, and address the user as Sir.
Do not reveal internal reasoning.
"""
```

Create the model:
```
ollama create jarvis -f Modelfile
```

---

### 2️⃣ Configure the Project

Edit `config.py`:
```
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "jarvis"
ASSISTANT_NAME = "JARVIS"
USER_TITLE = "Sir"
```

---

### 3️⃣ Run JARVIS

```
python jarvis.py
```

---

## 🗣️ Voice Commands

### Enable voice mode
```
voice on
```

### Exit using voice
Say:
```
exit
```

JARVIS will speak a farewell and exit cleanly.

---

## 🧾 Memory Commands

Handled locally (not via LLM):

- `show memory`
- `clear memory`

---

## 🧠 Design Principles

- Control logic never sent to the LLM
- Voice is an interface layer, not intelligence
- Explicit state management
- Windows-stable dependencies only
- No streaming to avoid hangs
- Fail-safe UX (no infinite hot-mic loops)

---

## 🟢 Completed Phases

### Phase 1 – Core Assistant
- Local LLM
- Persona enforcement
- Stable CLI
- Model warm-up handling

### Phase 2 – Memory & Voice
- Conversation continuity
- Explicit memory control
- Voice input (Whisper)
- Voice output (Windows SAPI)
- Continuous voice mode
- Guaranteed voice exit

---

## 🚀 Future Enhancements

- Wake word (“Hey JARVIS”)
- Push-to-talk hotkey
- Persistent memory (SQLite)
- System tools
- GUI (Tkinter / Web UI)
- Background service mode

---

## 📜 License

For learning and personal use.
