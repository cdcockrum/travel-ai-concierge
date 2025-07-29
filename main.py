from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class Prompt(BaseModel):
    message: str

@app.post("/chat")
def chat_with_ai(prompt: Prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant."},
                {"role": "user", "content": prompt.message}
            ]
        )
        return {"response": response['choices'][0]['message']['content']}
    except Exception as e:
        return {"error": str(e)}

