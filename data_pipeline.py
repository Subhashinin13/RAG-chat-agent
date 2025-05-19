import pandas as pd
import aiomysql
import asyncio

# Database configuration
DB_CONFIG = {
    'host': 'localhost',        
    'user': 'subha',             
    'password': 'subha@13',
    'db': 'federal_data',       
}

# Path to the processed data CSV file
processed_file_path = 'processed_data/processed_federal_data.csv'

# Load the processed CSV file
df = pd.read_csv(processed_file_path)

async def insert_data_to_mysql():
    # Create an asynchronous connection pool
    pool = await aiomysql.create_pool(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        db=DB_CONFIG['db'],
        minsize=1,   # Minimum number of connections in the pool
        maxsize=10,  # Maximum number of connections in the pool
    )

    async with pool.acquire() as conn:  
        async with conn.cursor() as cur:  
            await conn.begin()  

            try:
                # Preparing the SQL Query
                sql = """
                    INSERT INTO federal_registry (document_number, title, date, agency, url)
                    VALUES (%s, %s, %s, %s, %s)
                """

                data = [
                    (
                        row['document_number'], 
                        row['title'], 
                        row['date'], 
                        row['agency'], 
                        row['url']
                    ) 
                    for _, row in df.iterrows()
                ]

              
                await cur.executemany(sql, data)
                await conn.commit()  # Commit the transaction if successful
                print(f"Successfully inserted {len(data)} rows into the database.")
            
            except Exception as e:
                await conn.rollback() 
                print("Error occurred:", e)
            
    pool.close()
    await pool.wait_closed()


if __name__ == "__main__":
    asyncio.run(insert_data_to_mysql())
