import mysql.connector

def get_federal_data(topic: str, date: str) -> str:
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="subha",
            password="subha@13",
            database="federal_data"
        )
        cursor = connection.cursor()

        query = """
        SELECT title, publication_date
        FROM federal_register
        WHERE title LIKE %s AND publication_date LIKE %s
        ORDER BY publication_date DESC
        LIMIT 5
        """
        cursor.execute(query, (f"%{topic}%", f"{date}-%"))
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        if not results:
            return "No documents found."
        return "\n".join(f"{title} ({date})" for title, date in results)

    except Exception as e:
        return f"Error accessing database: {str(e)}"
