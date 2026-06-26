import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.database import get_db_connection

def save_commit_record(developer_name: str, commit_sha: str, commit_message: str, commited_at: str):
    query = """
        INSERT INTO velocity_metrics (developer_name, commit_sha, commit_message, committed_at)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (commit_sha) DO NOTHING;
    """
    connection = get_db_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (developer_name, commit_sha, commit_message, committed_ai))
            connection.commit()
            return True
    except Exception as e:
        print(f"DAO Error saving record: {e}")
        connection.rollback()
        return False
    finally: 
        connection.close()
    
def check_inactivity_status():
    query = """
        SELECT 
            NOW() - MAX(committed_at) AS time_since_last_commit,
            CASE
                WHEN NOW() - MAX(committed_at) > INTERVAL '72 hours' THEN TRUE
                ELSE FALSE
            END AS is_threshold_breached
        FROM velocity_metrics;
    """

    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            resutl = cursor.fetchone()

            if not result or result[0] is None:
                return {"hours_elapsed": 0, "breached": False, "empty_db": True}
            
            time_delta = result[0]
            hourse_elapse - int(time_delta.total_seconds() / 3600)

            return {
                "hours_elapsed": hours_elapsed,
                "breached": result[1],
                "empty_db": False
            }
    except Exception as e:
        print(f"DAO Error calculating threshold: {e}")
        return None
    finally:
        connection.close()