
import os
import tempfile
import threading
import importlib
import json
from urllib.request import Request, urlopen

lock = threading.Lock()

TTS_URL = "http://127.0.0.1:5055/speak"  # Replace with your TTS server URL


def speak(text):
    print("Jarvis:", text)

    with lock:
        audio_file = None

        try:
            request = Request(
                TTS_URL,
                data=json.dumps({"text": text}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(request, timeout=180) as response:
                audio_data = response.read()

            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False
            ) as temp:
                audio_file = temp.name
                temp.write(audio_data)

            pygame = importlib.import_module("pygame")
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(30)

            pygame.mixer.music.unload()

        except Exception as e:
            print("JARVIS VOICE ERROR:", e)

        finally:
            if audio_file and os.path.exists(audio_file):
                try:
                    os.remove(audio_file)
                except OSError:
                    pass
