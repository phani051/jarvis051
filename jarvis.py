# jarvis.py
# CLI entry point for JARVIS (Phase 2 + Voice Mode)

from brain import ask_jarvis
from model_loader import wait_for_model_ready
from memory import get_memory, clear_memory, has_memory
from voice import listen, speak
from config import ASSISTANT_NAME, EXIT_COMMANDS, USER_TITLE


def main():
    voice_mode = False          # 🔊 Voice mode flag
    silence_count = 0           # 🛑 Silence tracker
    MAX_SILENCE = 3

    print("=" * 60)
    print(f"🔄 Initializing {ASSISTANT_NAME}...")
    print("Please wait while the model is loading.")
    print("=" * 60)

    try:
        wait_for_model_ready()
    except Exception as e:
        print(f"\n❌ Failed to initialize {ASSISTANT_NAME}: {e}")
        return

    print("\n" + "=" * 60)
    print(f"✅ {ASSISTANT_NAME} online.")
    print(f"Awaiting your command, {USER_TITLE}.")
    print("Commands:")
    print(" - voice on     → enable voice mode")
    print(" - bye / exit   → spoken or typed exit")
    print(" - show memory")
    print(" - clear memory")
    print("=" * 60)

    while True:
        try:
            # 🎤 Voice Mode
            if voice_mode:
                spoken_text = listen()
                command = spoken_text.lower().strip() if spoken_text else ""

                # 🔴 EXIT ALWAYS HAS PRIORITY
                if command in EXIT_COMMANDS:
                    farewell = f"Goodbye, {USER_TITLE}. Have a great day."
                    print(f"\n{ASSISTANT_NAME}: {farewell}")
                    speak(farewell)
                    break

                # 🛑 Handle silence
                if not command:
                    silence_count += 1
                    print("\nI did not catch that, sir.")

                    if silence_count >= MAX_SILENCE:
                        standby = f"I am standing by, {USER_TITLE}."
                        print(f"\n{ASSISTANT_NAME}: {standby}")
                        speak(standby)
                        voice_mode = False
                        silence_count = 0
                    continue

                # Reset silence counter on valid speech
                silence_count = 0
                print(f"\nYou said: {spoken_text}")
                user_input = spoken_text

            else:
                user_input = input("\n> ").strip()
                if not user_input:
                    continue
                command = user_input.lower()

            # 🔹 Typed exit (text mode)
            if command in EXIT_COMMANDS:
                farewell = f"Goodbye, {USER_TITLE}. Have a great day."
                print(f"\n{ASSISTANT_NAME}: {farewell}")
                break

            # 🔹 Voice mode toggle (typed only)
            if command == "voice on":
                voice_mode = True
                silence_count = 0
                print("\n🎤 Voice mode enabled.")
                continue

            # 🔹 Memory commands
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

            # 🔹 Normal LLM processing
            response = ask_jarvis(user_input)
            print(f"\n{response}")

            if voice_mode:
                speak(response)

        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{ASSISTANT_NAME} interrupted. Standing down, {USER_TITLE}.")
            break

        except Exception as e:
            print(f"\nApologies, {USER_TITLE}. An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
