from api_resource import FastAPI, Request
from pydantic import BaseModel
import openai
import asyncio
import json
from source import run_agent  # Assuming run_agent handles agent logic including tool calls

# Point OpenAI client to local Ollama
openai.api_key = "ollama"  # required but ignored by Ollama
openai.base_url = "http://localhost:11434/v1"

app = FastAPI()

# Input schema for the /chat endpoint
class ChatRequest(BaseModel):
    user_query: str

# Output schema (optional, for clarity)
class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Send the user query to the agent handler (in source.py)
        response = await run_agent(request.user_query)
        return {"response": response}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
