import openai
import asyncio

# ✅ Configure for Ollama
openai.api_base = "http://localhost:11434/v1"
openai.api_key = "ollama"  # Dummy key, required by OpenAI client

# ✅ Minimal async chat function
async def run_agent(user_query: str) -> str:
    messages = [{"role": "user", "content": user_query}]

    response = openai.ChatCompletion.create(
        model="qwen:0.5b",
        messages=messages
    )

    reply = response["choices"][0]["message"]["content"]
    return reply

# ✅ For CLI testing
if __name__ == "__main__":
    query = input("Ask your question: ")
    result = asyncio.run(run_agent(query))
    print("\nModel replied:", result)
