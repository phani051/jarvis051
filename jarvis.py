# jarvis.py
# CLI entry point for JARVIS (Phase 2 + Voice, Windows-safe)

from brain import ask_jarvis
from model_loader import wait_for_model_ready
from memory import get_memory, clear_memory, has_memory
from voice import listen, speak
from config import ASSISTANT_NAME, EXIT_COMMANDS, USER_TITLE


def main():
    print("=" * 60)
    print(f"🔄 Initializing {ASSISTANT_NAME}...")
    print("Please wait while the model is loading.")
    print("=" * 60)

    try:
        # Block until the model responds at least once
        wait_for_model_ready()
    except Exception as e:
        print(f"\n❌ Failed to initialize {ASSISTANT_NAME}: {e}")
        return

    print("\n" + "=" * 60)
    print(f"✅ {ASSISTANT_NAME} online.")
    print(f"Awaiting your command, {USER_TITLE}.")
    print("Commands:")
    print(" - voice        → speak your prompt")
    print(" - show memory  → view conversation memory")
    print(" - clear memory → reset conversation memory")
    print(" - exit / quit / bye")
    print("=" * 60)

    while True:
        try:
            user_input = input("\n> ").strip()

            if not user_input:
                continue

            command = user_input.lower()

            # 🔹 Exit commands
            if command in EXIT_COMMANDS:
                print(f"\n{ASSISTANT_NAME} signing off. Goodbye, {USER_TITLE}.")
                break

            # 🔹 Memory commands (handled locally)
            if command == "show memory":
                if has_memory():
                    print("\n" + get_memory())
                else:
                    print("\nNo conversation memory available.")
                continue

            if command == "clear memory":
                clear_memory()
                print("\nConversation memory cleared.")
                continue

            # 🔹 Voice input mode
            if command == "voice":
                spoken_text = listen()

                if not spoken_text:
                    print("\nI did not catch that, sir.")
                    continue

                print(f"\nYou said: {spoken_text}")
                response = ask_jarvis(spoken_text)
                print(f"\n{response}")
                speak(response)
                continue

            # 🔹 Normal text input mode
            response = ask_jarvis(user_input)
            print(f"\n{response}")

        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{ASSISTANT_NAME} interrupted. Standing down, {USER_TITLE}.")
            break

        except Exception as e:
            print(f"\nApologies, {USER_TITLE}. An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
