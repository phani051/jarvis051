# memory.py
# Short-term conversation memory for JARVIS

MAX_TURNS = 6   # total messages (user + assistant)

_memory = []


def add_message(role: str, content: str):
    _memory.append(f"{role}: {content}")

    if len(_memory) > MAX_TURNS:
        _memory.pop(0)


def get_memory() -> str:
    if not _memory:
        return ""

    return "CONVERSATION HISTORY:\n" + "\n".join(_memory)


def clear_memory():
    _memory.clear()


def has_memory() -> bool:
    return len(_memory) > 0
