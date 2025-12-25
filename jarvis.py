# jarvis.py
# CLI entry point for JARVIS (Phase 1)

from brain import ask_jarvis
from model_loader import wait_for_model_ready
from config import ASSISTANT_NAME, EXIT_COMMANDS, USER_TITLE


def main():
    print("=" * 60)
    print(f"🔄 Initializing {ASSISTANT_NAME}...")
    print("Please wait while the model is loading.")
    print("=" * 60)

    try:
        # ⬅️ BLOCK HERE until model is fully ready
        wait_for_model_ready()

    except Exception as e:
        print(f"\n❌ Failed to initialize {ASSISTANT_NAME}: {e}")
        return

    print("\n" + "=" * 60)
    print(f"✅ {ASSISTANT_NAME} online.")
    print(f"Awaiting your command, {USER_TITLE}.")
    print("Type 'exit', 'quit', or 'bye' to end.")
    print("=" * 60)

    while True:
        try:
            user_input = input("\n> ").strip()

            if not user_input:
                continue

            if user_input.lower() in EXIT_COMMANDS:
                print(f"\n{ASSISTANT_NAME} signing off. Goodbye, {USER_TITLE}.")
                break

            response = ask_jarvis(user_input)
            print(f"\n{response}")

        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{ASSISTANT_NAME} interrupted. Standing down, {USER_TITLE}.")
            break

        except Exception as e:
            print(f"\nApologies, {USER_TITLE}. An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
