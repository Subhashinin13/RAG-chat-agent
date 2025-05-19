import openai
import mysql.connector
import json

# ✅ Client initialization (new style)
client = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# ✅ Tool function
def search_documents_by_president_and_date(president: str, year: int) -> str:
    conn = mysql.connector.connect(
        host="localhost",
        user="subha",
        password="subha@13",
        database="federal_data"
    )
    cursor = conn.cursor()
    query = """
        SELECT title, publication_date
        FROM federal_register
        WHERE president = %s AND YEAR(publication_date) = %s
    """
    cursor.execute(query, (president, year))
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    if not results:
        return "No documents found."
    return "\n".join([f"{title} ({date})" for title, date in results])

# ✅ Tool registration
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_documents_by_president_and_date",
            "description": "Search federal register documents by president and year.",
            "parameters": {
                "type": "object",
                "properties": {
                    "president": {"type": "string"},
                    "year": {"type": "integer"}
                },
                "required": ["president", "year"]
            }
        }
    }
]

# ✅ Conversation start
messages = [{"role": "user", "content": "List executive orders by Barack Obama in 2016"}]

# ✅ First response (tool call expected)
response = openai.ChatCompletion.create(
    model="mistral:7b-instruct",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message
tool_calls = message.tool_calls

# ✅ Handle tool call
if tool_calls:
    tool_call = tool_calls[0]
    func_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    if func_name == "search_documents_by_president_and_date":
        result = search_documents_by_president_and_date(**args)

        # ✅ Respond with function output
        followup = openai.ChatCompletion.create(
            model="mistral:7b-instruct",
            messages=[
                {"role": "user", "content": messages[0]["content"]},
                {"role": "assistant", "tool_calls": [tool_call]},
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": func_name,
                    "content": result
                }
            ]
        )

        print("\n✅ Final Answer:")
        print(followup.choices[0].message.content)
else:
    print("\n⚠️ No tool call made:")
    print(message.content)
