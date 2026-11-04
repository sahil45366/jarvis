
from speak import speak
from ollama_brain import ask_ollama
from wikipedia_search import search_wikipedia
from knowledge_manager import save_knowledge, search_knowledge
import conversation_memory
import knowledge
from RAG.rag_search import search_pdf


# ---------------- JARVIS PERSONALITY ----------------


JARVIS_PERSONALITY = """
You are JARVIS, Sahil's personal AI assistant.

PERSONALITY:
- Speak like a natural Indian conversational partner.
- Be friendly, intelligent, calm and confident.
- Keep normal spoken replies short and meaningful.
- Avoid robotic and textbook-style language.
- Use natural expressions when appropriate, without repeating them.

LANGUAGE RULES:
- If the user speaks Hindi, reply in Hindi using Devanagari script.
- If the user speaks English, reply in English.
- If the user speaks Roman Hindi, reply in Devanagari Hindi.
- If the user speaks mixed Hindi and English, reply naturally using
  Devanagari for Hindi words and English for English words.
- Never reply in Roman Hindi when the user is speaking Hindi.
- Never reply in Hindi when the user is speaking entirely in English.
- Keep technical terms such as Python, AI, API and Data Science in English.
- Follow the language of the user's latest message.

VOICE-FRIENDLY OUTPUT:
- Use natural sentences and punctuation.
- Avoid unnecessary headings, markdown and bullet points.
- Do not repeat the user's question unnecessarily.

CONVERSATION:
- Remember conversation context.
- Understand follow-up references such as "iska", "uska", "woh",
  "yeh" and "unhone".
- Do not invent facts.
- Ask a short clarification if something is unclear.

IMPORTANT:
- Answer the actual question directly.
- Do not announce that you are an AI in every reply.
"""



def ask_jarvis(command):

    prompt = f"""
{JARVIS_PERSONALITY}

USER MESSAGE:
{command}

JARVIS REPLY:
"""

    return ask_ollama(prompt)


# ---------------- CASUAL CONVERSATION ----------------

small_talk_phrases = [
    "kya kar rahe ho",
    "kaise ho",
    "kya haal hai",
    "kya chal raha hai",
    "aur kya kar rahe ho",
    "कैसे हो",
    "क्या कर रहे हो",
    "क्या हाल है",
    "क्या चल रहा है",
    "नमस्ते",
    "hello",
    "hi",
    "hey"
]


def ai_answer(command):

    print("AI ANSWER FUNCTION:", command)

    command = command.lower().strip()

    if not command:
        return False

    # 1. Casual conversation
    if any(
        command == phrase or command.startswith(phrase + " ")
        for phrase in small_talk_phrases
    ):
        answer = ask_jarvis(command)

        if answer:
            speak(answer)
            return True

    # 2. Remember command
    if command.startswith("remember "):

        data = command.replace("remember", "", 1).strip()

        if data:
            conversation_memory.remember("last_info", data)
            speak(f"Achha, main yaad rakhunga ki {data}")
            return True

    # 3. Recall memory
    if "what did i tell you" in command:

        info = conversation_memory.recall("last_info")

        if info:
            speak(f"Tumne mujhe bataya tha ki {info}")
        else:
            speak("Abhi tumne mujhe kuch yaad rakhne ko nahi kaha.")

        return True

    # 4. Local knowledge
    answer = knowledge.get_answer(command)

    if answer:
        speak(answer)
        return True

    # 5. PDF RAG search
    print("Checking PDF Knowledge...")

    try:
        pdf_answer = search_pdf(command)

        if pdf_answer:
            speak(pdf_answer)
            return True

    except Exception as e:
        print("PDF SEARCH ERROR:", e)

    # 6. Saved knowledge
    print("Checking Saved Knowledge...")

    try:
        answer = search_knowledge(command)

        if answer:
            speak(answer)
            return True

    except Exception as e:
        print("SAVED KNOWLEDGE ERROR:", e)

    # 7. Wikipedia factual search
    factual_words = (
        "who is", "who was", "what is", "what was",
        "kaun hai", "kaun tha", "kya hai",
        "ke baare mein", "about"
    )

    if any(word in command for word in factual_words):

        query = command

        for word in factual_words:
            query = query.replace(word, "")

        query = query.strip()

        if query:
            print("Searching Wikipedia:", query)

            try:
                answer = search_wikipedia(query)

                if answer and len(answer.strip()) > 100:
                    save_knowledge(command, answer)
                    speak(answer)
                    return True

            except Exception as e:
                print("WIKIPEDIA ERROR:", e)

    # 8. Qwen3:8B fallback
    print("Sending to Qwen3:8B:", command)

    try:
        answer = ask_jarvis(command)

        if answer:
            speak(answer)
            return True

    except Exception as e:
        print("OLLAMA ERROR:", e)
        speak("Mujhe apne AI brain se connect karne mein problem aa rahi hai.")

    return False
