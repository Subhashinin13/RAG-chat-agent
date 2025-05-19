import pandas as pd
import aiomysql
import asyncio

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',        # MySQL host (default is localhost)
    'user': 'subha',             # Your MySQL username
    'password': 'subha@13',# Your MySQL password
    'db': 'federal_data',       # Your MySQL database name
}

# Path of the processed CSV file
processed_file_path = 'processed_data/processed_federal_data.csv'

# Read the processed CSV file
df = pd.read_csv(processed_file_path)

# Async function to insert data into MySQLhh
async def insert_data_to_mysql():
    # Create an asynchronous connection pool
    pool = await aiomysql.create_pool(**DB_CONFIG)

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            for _, row in df.iterrows():
                # Prepare the SQL insert query
                sql = """
                    INSERT INTO federal_registry (document_number, title, date, agency, url)
                    VALUES (%s, %s, %s, %s, %s)
                """
                # Execute the query for each row
                await cur.execute(sql, (
                    row['document_number'], 
                    row['title'], 
                    row['date'], 
                    row['agency'], 
                    row['url']
                ))
            await conn.commit()  # Commit the transaction

    pool.close()
    await pool.wait_closed()

# Run the insertion function
asyncio.run(insert_data_to_mysql())
