
import requests
import conversation_memory
import re
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:8b"

FOLLOW_UP_WORDS = {
    "inhone", "unhone", "iska", "isne",
    "ye", "woh", "usne", "unka",
    "iske", "usse", "uska", "unki"
}

SMALL_TALK = [
    "kaise ho",
    "kya haal hai",
    "aur kya kar rahe ho",
    "kya kar rahe ho",
    "kya chal raha hai",
    "hello",
    "hi",
    "hey",
    "good morning",
    "good evening"
]

STOP_WORDS = {
    "kaun", "kya", "hai", "ho", "tha", "the",
    "karo", "kar", "rahe", "raha", "rahi",
    "kiya", "inhone", "unhone", "ye", "woh",
    "iska", "isne", "batao", "samjhao",
    "mujhe", "ke", "ki", "ka", "ko",
    "mein", "par", "aur", "se", "kaise",
    "aap", "tum", "main"
}


def clean_text(text):
    return re.sub(r"[^\w\s]", "", text.lower()).strip()


def is_follow_up(text):
    words = set(clean_text(text).split())
    return bool(words.intersection(FOLLOW_UP_WORDS))


def is_small_talk(text):
    cleaned = clean_text(text)

    return any(
        phrase in cleaned
        for phrase in SMALL_TALK
    )


def extract_topic(text):
    words = clean_text(text).split()

    topic_words = [
        word for word in words
        if word not in STOP_WORDS
    ]

    return " ".join(topic_words).strip()


def ask_ollama(prompt):

    start_time = time.perf_counter()

    try:
        history = conversation_memory.get_conversation()

        active_topic = (
            conversation_memory.recall("active_topic") or ""
        )

        small_talk = is_small_talk(prompt)

        if small_talk:
            current_topic = ""

        elif is_follow_up(prompt) and active_topic:
            current_topic = active_topic

        else:
            current_topic = extract_topic(prompt)

        system_prompt = f"""
You are JARVIS, Sahil's personal AI assistant.

LANGUAGE:
- Speak natural Hinglish in Roman Hindi.
- Use English technical terms when needed.

PERSONALITY:
- Friendly, intelligent and logical.
- Do not blindly agree.
- Correct mistakes politely.

CONVERSATION:
- Understand conversation history and follow-up references.
- Do not repeat the user's question.
- Respond naturally to casual conversation.

ACCURACY:
- Answer the exact question asked.
- Never answer with an unrelated date or fact.
- Do not confuse similar-sounding words.
- For definitions, give a direct definition first.
- For translation, provide the correct English word.
- Use conversation history only when the current question needs it.
- Never invent information.
- If unsure, clearly say so.

RESPONSE LENGTH:
- Normal answers: 2-4 sentences.
- Technical questions: explain clearly but concisely.
- Avoid unnecessary repetition.

CURRENT QUESTION:
{prompt}

PREVIOUS TOPIC (use only if relevant):
{current_topic}

CONVERSATION HISTORY:
{history}

USER MESSAGE:
{prompt}

Give only the final answer.
"""

        response = requests.post(
            OLLAMA_URL,
            json={
    "model": MODEL_NAME,
    "prompt": system_prompt,
    "stream": False,
    "think": False,
    "keep_alive": "10m",
    "options": {
        "temperature": 0.5,
        "num_predict": 250,
        "num_ctx": 4096
    }
},
            timeout=180
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get("response", "").strip()

        if not answer:
          print("QWEN EMPTY RESPONSE")
          print("Thinking:", data.get("thinking", ""))
          print("Done reason:", data.get("done_reason"))

          return "Mujhe answer generate karne mein problem hui."  

        conversation_memory.save_conversation(
            prompt,
            answer
        )

        if not small_talk and current_topic:
            conversation_memory.remember(
                "active_topic",
                current_topic
            )

        elapsed = time.perf_counter() - start_time
        print(f"Qwen response time: {elapsed:.2f} seconds")

        return answer

    except requests.exceptions.ConnectionError:
        print("JARVIS ERROR: Ollama is not running.")
        return "Ollama se connection nahi ho raha."

    except requests.exceptions.Timeout:
        print("JARVIS ERROR: Request timeout.")
        return "Response aane mein time lag raha hai."

    except Exception as e:
        print("JARVIS ERROR:", e)
        return None
