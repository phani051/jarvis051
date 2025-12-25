# config.py
# Central configuration for JARVIS Phase 1

# Ollama settings
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "jarvis"   # your qwen3-vl based JARVIS model

# Assistant identity
ASSISTANT_NAME = "JARVIS"
USER_TITLE = "Sir"

# Response behavior
DEFAULT_TEMPERATURE = 0.2
DEFAULT_TOP_P = 0.9
REPEAT_PENALTY = 1.1

# CLI behavior
EXIT_COMMANDS = {"exit", "quit", "bye"}
