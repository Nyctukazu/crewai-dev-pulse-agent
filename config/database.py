import os
import psycopg2
from dotenv import load_load

load_dotenv()

def get_db_connection():
    try:
        connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        return connection
    except Exception as e:
        print(f"Database Connection Error: {e}")
        return None