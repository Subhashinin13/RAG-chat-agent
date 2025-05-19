from fastapi import FastAPI
from pydantic import BaseModel
from agent_logic import ask_llm  # ✅ import this

app = FastAPI()

class ChatRequest(BaseModel):
    user_query: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    response = await ask_llm(request.user_query)
    return {"response": response}
