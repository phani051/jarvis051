# brain.py
# Handles communication with Ollama (JARVIS brain)

import requests
from config import (
    OLLAMA_URL,
    MODEL_NAME,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
    REPEAT_PENALTY,
)
from context import get_system_context



def warm_up_model():
    """
    Sends a lightweight request to warm up the model.
    """
    try:
        requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": "ping",
                "stream": False,
                "options": {"num_predict": 1}
            },
            timeout=120
        )
    except Exception:
        pass


def ask_jarvis(user_query: str) -> str:
    """
    Sends a prompt to Ollama and returns JARVIS's response.
    """
    _MODEL_WARMED = False

    if not _MODEL_WARMED:
        warm_up_model()
        _MODEL_WARMED = True

    system_context = get_system_context()

    prompt = f"""
{system_context}

ROLE:
You are JARVIS, the advanced AI assistant.
Stay in character at all times.

INSTRUCTIONS (IMPORTANT):
- Respond ONLY with the final answer.
- Do NOT show reasoning, thinking, or analysis.
- Be concise, clear, and professional.
- Address the user as 'Sir'.

USER QUERY:
{user_query}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt.strip(),
        "stream": False,
        "keep_alive": "10m",
        "options": {
            "temperature": DEFAULT_TEMPERATURE,
            "top_p": DEFAULT_TOP_P,
            "repeat_penalty": REPEAT_PENALTY
        },
    }

    try:
        response = requests.post(
    OLLAMA_URL,
    json=payload,
    timeout=300,
    stream=False
)
        response.raise_for_status()

        data = response.json()
        return data.get("response", "").strip()

    except requests.exceptions.RequestException as e:
        return f"Apologies, sir. I encountered a communication error: {e}"

