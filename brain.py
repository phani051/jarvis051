# brain.py
# Inference only – no lifecycle logic

import requests
from config import (
    OLLAMA_URL,
    MODEL_NAME,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
    REPEAT_PENALTY,
    USER_TITLE,
)
from context import get_system_context


def ask_jarvis(user_query: str) -> str:
    system_context = get_system_context()

    prompt = f"""
{system_context}

ROLE:
You are JARVIS.

INSTRUCTIONS:
- Respond ONLY with the final answer
- Be concise and professional
- Address the user as '{USER_TITLE}'

USER QUERY:
{user_query}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt.strip(),
        "stream": False,
        # 🔑 keep_alive belongs here (usage-time), NOT loading-time
        "keep_alive": "30m",
        "options": {
            "temperature": DEFAULT_TEMPERATURE,
            "top_p": DEFAULT_TOP_P,
            "repeat_penalty": REPEAT_PENALTY,
        },
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=600,
    )
    response.raise_for_status()

    # NDJSON-safe parse (recommended)
    raw = response.text.strip()
    last = raw.splitlines()[-1]

    import json
    return json.loads(last).get("response", "").strip()
