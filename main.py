from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

app = FastAPI()

class Prompt(BaseModel):
    message: str

@app.post("/chat")
def chat_with_groq(prompt: Prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a helpful travel assistant."},
            {"role": "user", "content": prompt.message}
        ]
    }

    response = requests.post(GROQ_URL, json=payload, headers=headers)

    if response.status_code != 200:
        return {"error": response.text}

    result = response.json()
    return {"response": result["choices"][0]["message"]["content"]}
