# brain.py
# Inference engine for JARVIS (Phase 2)
# - Uses short-term conversation memory
# - No lifecycle or warm-up logic

import requests
import json

from config import (
    OLLAMA_URL,
    MODEL_NAME,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
    REPEAT_PENALTY,
    USER_TITLE,
)
from context import get_system_context
from memory import get_memory, add_message


def ask_jarvis(user_query: str) -> str:
    """
    Sends a prompt to Ollama and returns JARVIS's response.
    Conversation memory is injected for continuity.
    """

    # Gather context
    system_context = get_system_context()
    conversation_history = get_memory()

    # Build prompt
    prompt = f"""
{system_context}

{conversation_history}

ROLE:
You are JARVIS, the advanced AI assistant.

INSTRUCTIONS:
- Respond ONLY with the final answer
- Do NOT reveal reasoning or internal thoughts
- Maintain conversational continuity
- Be concise, clear, and professional
- Address the user as '{USER_TITLE}'

USER QUERY:
{user_query}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt.strip(),
        "stream": False,
        # Keep model alive between turns
        "keep_alive": "30m",
        "options": {
            "temperature": DEFAULT_TEMPERATURE,
            "top_p": DEFAULT_TOP_P,
            "repeat_penalty": REPEAT_PENALTY,
        },
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300,
        )
        response.raise_for_status()

        # Ollama may return NDJSON; parse last JSON object
        raw_text = response.text.strip()
        last_line = raw_text.splitlines()[-1]
        data = json.loads(last_line)

        answer = data.get("response", "").strip()

        # Update conversation memory AFTER response
        add_message("User", user_query)
        add_message("JARVIS", answer)

        return answer

    except requests.exceptions.RequestException as e:
        return f"Apologies, {USER_TITLE}. I encountered a communication error: {e}"

    except json.JSONDecodeError:
        return f"Apologies, {USER_TITLE}. I received an unreadable response from the model."
