from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .chat import chat

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

    try:
        response = chat(user_message, history)
        return {"response": response}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
