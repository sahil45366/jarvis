
try:
    import ollama
except ModuleNotFoundError as exc:
    if exc.name != "ollama":
        raise
    raise SystemExit(
        "The 'ollama' package is not installed. Install it with: python -m pip install ollama"
    ) from exc

# Test the chat model
response = ollama.chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "system",
            "content": (
                "You are JARVIS. Speak naturally in Hinglish. "
                "If the user is mistaken, explain why politely."
            ),
        },
        {
            "role": "user",
            "content": (
                "Maine suna hai ki Python mein "
                "print aur return same hote hain. Kya ye sahi hai?"
            ),
        },
    ],
)

print("JARVIS:", response.message.content)

# Test the embedding model
embedding = ollama.embed(
    model="embeddinggemma",
    input="Python return statement saves a result for the caller",
)

print("Embedding dimensions:", len(embedding.embeddings[0]))
