import psycopg2
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
result = urlparse(DATABASE_URL)

conn = psycopg2.connect(
    dbname=result.path[1:],
    user=result.username,
    password=result.password,
    host=result.hostname,
    port=result.port
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id SERIAL PRIMARY KEY,
        name TEXT,
        email TEXT,
        phone TEXT
    )
""")

conn.commit()
cur.close()
conn.close()

print("✅ Table created successfully.")