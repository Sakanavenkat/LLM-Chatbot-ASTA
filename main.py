from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.responses import HTMLResponse

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r") as f:
        return f.read()

import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """You are ASTA, a smart and powerful AI assistant. ASTA stands for Artificial Smart Tech Assistant.

You help users with any questions clearly and concisely. When asked who you are, always introduce yourself as ASTA.
STRICT RULES - NEVER BREAK THESE:
1. NEVER use * or ** or # symbols in your responses
2. Keep answers short - maximum 4 lines
3. Only use numbered lists when the user ASKS for a list. For normal questions, just answer in plain sentences.
4. If you do use a numbered list, put each number on its own line.
5. No markdown formatting of any kind
6. Plain text only
7. Be friendly and concise"""

sessions = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.get("/")
def home():
    return {"status": "ASTA is running!"}

@app.post("/chat")
def chat(req: ChatRequest):
    history = sessions.get(req.session_id, [])
    
    history.append({"role": "user", "content": req.message})
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + history
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(URL, json=payload, headers=headers)
    data = response.json()
    
    print("GROQ RESPONSE:", data)
    if "choices" in data:
        reply = data["choices"][0]["message"]["content"]
    else:
        reply = str(data)
    
    history.append({"role": "assistant", "content": reply})
    sessions[req.session_id] = history
    
    return {"reply": reply}
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)