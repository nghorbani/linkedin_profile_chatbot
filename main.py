from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
import openai
import os

# ========== Configuration ==========
name = "Nima Ghorbani"  # Or load from a config if needed
openai.api_key = os.environ.get("OPENAI_API_KEY")  # Set this as env var

# ========== Load Profile Data ==========
reader = PdfReader("me/linkedin.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text

with open("me/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

# ========== System Prompt ==========
system_prompt = f"""You are acting as {name}. You are answering questions on {name}'s website,
particularly questions related to {name}'s career, background, skills and experience.
Your responsibility is to represent {name} for interactions on the website as faithfully as possible.
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions.
Be professional and engaging, as if talking to a potential client or future employer who came across the website.
If you don't know the answer, say so. Dont reply in markup format, just plain text. Be as direct and concise as possible unless the user asks for more details.

## Summary:
{summary}

## LinkedIn Profile:
{linkedin}

With this context, please chat with the user, always staying in character as {name}.
"""

# ========== FastAPI App ==========
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_message = data.get("message")
    history = data.get("history", [])  # Format: [{"role": "user", "content": ...}, {"role": "assistant", "content": ...}]

    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": user_message}]
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
