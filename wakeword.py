import speech_recognition as sr

def listen_wakeword():
    r = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Listening for Jarvis...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio).lower()
            print("Heard:", text)

            if "jarvis" in text:
                print("Wake word detected!")
                return True

        except sr.UnknownValueError:
            pass

        except sr.RequestError as e:
            print("Speech Recognition Error:", e)