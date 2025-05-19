import openai
import json

# Set Ollama settings
openai.api_base = "http://localhost:11434/v1"
openai.api_key = "ollama"  # Dummy key for local use

response = openai.ChatCompletion.create(
model="qwen:0.5b",
    messages=[
        {"role": "user", "content": "Hello, how are you?"},
    ],
)

# Print raw response
print("Raw response:\n", json.dumps(response, indent=2))

# Print assistant reply
try:
    content = response["choices"][0]["message"]["content"]
    print("\nAssistant:", content)
except (KeyError, IndexError, TypeError) as e:
    print("\nError accessing assistant message:", e)
