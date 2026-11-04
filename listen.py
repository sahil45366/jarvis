
import speech_recognition as sr
import re

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


def has_devanagari(text):
    return any("\u0900" <= ch <= "\u097F" for ch in text)


def has_latin(text):
    return any("a" <= ch.lower() <= "z" for ch in text)


def roman_hindi_to_devanagari(text):
    try:
        return transliterate(
            text,
            sanscript.ITRANS,
            sanscript.DEVANAGARI
        )
    except Exception as e:
        print("Transliteration error:", e)
        return text


def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def select_best_transcript(hindi, english):

    hindi = clean_text(hindi)
    english = clean_text(english)

    if not hindi:
        return english

    if not english:
        if has_devanagari(hindi):
            return hindi
        return roman_hindi_to_devanagari(hindi)

    # Hindi recognizer returned Roman text
    if not has_devanagari(hindi):
        return english if english else roman_hindi_to_devanagari(hindi)

    # If both recognizers produce similar text,
    # prefer the script from the Hindi recognizer.
    hindi_words = hindi.split()
    english_words = english.split()

    # A short English transcript is often better than
    # a Hindi transcript containing English words phonetically.
    if len(english_words) > 0 and len(hindi_words) > 0:

        english_ratio = sum(
            1 for word in english_words
            if any(ch.isalpha() and ord(ch) < 128 for ch in word)
        ) / len(english_words)

        if english_ratio >= 0.8:
            return english

    return hindi


def listen_command():

    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8

    with sr.Microphone() as source:

        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = r.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        except sr.WaitTimeoutError:
            return ""

    hindi_result = ""
    english_result = ""

    # Hindi recognition
    try:
        hindi_result = r.recognize_google(
            audio,
            language="hi-IN"
        ).strip()

    except sr.UnknownValueError:
        pass

    except sr.RequestError:
        print("Hindi recognition service unavailable.")

    # English recognition
    try:
        english_result = r.recognize_google(
            audio,
            language="en-IN"
        ).strip()

    except sr.UnknownValueError:
        pass

    except sr.RequestError:
        print("English recognition service unavailable.")

    print("Hindi result:", hindi_result)
    print("English result:", english_result)

    command = select_best_transcript(
        hindi_result,
        english_result
    )

    if not command:
        print("Sorry, I did not understand.")
        return ""

    command = command.strip()

    # Remove wake word
    if command.lower().startswith("jarvis"):
        command = command[len("jarvis"):].strip()

    corrections = {
        "c plus plus": "C++",
        "c plus": "C++",
        "cpp": "C++"
    }

    for old, new in corrections.items():
        command = command.replace(old, new)

    print("Command:", command)

    return command
