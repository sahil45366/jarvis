from wakeword import listen_wakeword
from listen import listen_command
from speak import speak
from brain import brain
from multi_command import split_commands
import traceback


def main():

    speak("Jarvis is online")

    while True:

        # Wake word
        listen_wakeword()
        speak("Yes Sahil")

        # Commands
        while True:

            try:
                command = listen_command()

                if not command:
                    continue

                print("You said:", command)

                # Stop listening
                if "stop listening" in command.lower():
                    speak("Okay, waiting for wake word.")
                    break

                commands = split_commands(command)

                print("Split Commands:", commands)

                stop_requested = False

                for cmd in commands:

                    print("Executing:", cmd)

                    result = brain(cmd)

                    if result == "STOP_LISTENING":
                        stop_requested = True
                        break

                if stop_requested:
                    break

            except Exception:
                traceback.print_exc()


if __name__ == "__main__":
    main()