import json
import os


MEMORY_FILE = "memory.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError) as e:
            print("MEMORY LOAD ERROR:", e)

    return {}



def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)



def remember(key, value):

    memory = load_memory()

    memory[key] = value

    save_memory(memory)



def recall(key):

    memory = load_memory()

    return memory.get(key)



def save_conversation(user, assistant):

    memory = load_memory()


    if "conversation" not in memory:
        memory["conversation"] = []


    memory["conversation"].append(
        {
            "user": user,
            "assistant": assistant
        }
    )


    if len(memory["conversation"]) > 10:
        memory["conversation"].pop(0)


    save_memory(memory)



def get_conversation(limit=5):
    memory = load_memory()
    conversations = memory.get("conversation", [])
    return conversations[-limit:]



def save_topic(topic):

    remember(
        "last_topic",
        topic
    )



def get_topic():

    return recall("last_topic")
def save_context(user, language):

    memory = load_memory()

    if "context" not in memory:
        memory["context"] = []

    memory["context"].append(
        {
            "user": user,
            "language": language
        }
    )

    if len(memory["context"]) > 10:
        memory["context"].pop(0)

    save_memory(memory)