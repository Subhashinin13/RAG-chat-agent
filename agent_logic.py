import openai
import mysql.connector
import json

# Setup Ollama
openai.api_base = "http://localhost:11434/v1"
openai.api_key = "ollama"  # dummy key

# Define your MySQL tool
def run_query_tool(query: str):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="subha",
            password="subha@13",
            database="federal_data"
        )
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        return f"Error: {e}"

# 🧠 Agent logic that gets called from FastAPI
async def ask_llm(user_query: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant. If the user asks about federal data, suggest SQL or tool-based responses."},
        {"role": "user", "content": user_query}
    ]

    response = openai.ChatCompletion.create(
        model="qwen:0.5b",
        messages=messages
    )

    llm_reply = response["choices"][0]["message"]["content"]

    # --- Manual tool trigger based on keyword ---
    if "epa" in user_query.lower() and "rule" in user_query.lower():
        query = """
            SELECT title, publication_date
            FROM federal_register
            WHERE agency = 'Environmental Protection Agency'
            ORDER BY publication_date DESC
            LIMIT 5
        """
        result = run_query_tool(query)

        if isinstance(result, str):  # error message
            return result

        formatted = "\n".join([f"- {title} ({date})" for title, date in result])
        return f"Here are the latest EPA rules:\n{formatted}"

    # Otherwise return LLM reply directly
    return llm_reply
