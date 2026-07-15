import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        return connection
    except Exception as e:
        print(f"Database Connection Error: {e}")
        return None
    
def initialize_database():
    connection = get_db_connection()
    if not connection:
        print("Could not connect to database.  Aborting schema creation.")
        return
    
    create_project_table_query = """
    CREATE TABLE IF NOT EXIST project_info (
        id SERIAL PRIMARY KEY,
        project_name VARCHAR(255) NOT NULL,
        start_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        project_deadline TIMESTAMP NULL
    );
    """

    create_member_table_query = """
    CREATE TABLE IF NOT EXISTS member_info (
        name VARCHAR(255) PRIMARY KEY,
        roles VARCHAR(255) NOT NULL,
        status VARCHAR(50) DEFAULT 'ACTIVE',
        has_contributed_today BOOLEAN DEFAULT FALSE,
        last_active_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        project_id INTEGER REFERENCES project_info(id) ON DELETE CASCADE
    );
    """

    try:
        with connection.cursor() as cursor:
            print("Creating tables in Neon...")
            cursor.execute(create_project_table_query)
            cursor.execute(create_member_table_query)
            connection.commit()
            print("Database tables successfully created!")

    except Exception as e:
        print(f"Failed to create tables: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    initialize_database()