import requests

import os
API_KEY = os.environ.get("GROQ_API_KEY", "your-api-key-here")
URL = "https://api.groq.com/openai/v1/chat/completions"

history = []
SYSTEM_PROMPT = "You are ASTA, a smart and powerful AI assistant. ASTA stands for Artificial Smart Tech Assistant. You help users with any questions clearly and concisely. When asked who you are, always introduce yourself as ASTA."

print("Chatbot is ready! Type 'quit' to exit.")
print("-" * 40)

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    if user_input.strip() == "":
        continue

    history.append({"role": "user", "parts": [{"text": user_input}]})

    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": history
    }

    response = requests.post(URL, json=payload)
    data = response.json()

    if "candidates" in data:
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        history.append({"role": "model", "parts": [{"text": reply}]})
        print(f"Bot: {reply}")
        print()
    else:
        print(f"Error: {data}")
        break