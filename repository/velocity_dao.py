import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.database import get_db_connection

def save_commit_record(developer_name: str, commit_sha: str, commit_message: str, committed_at: str):
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

            print(f"Debug: Attempting to insert SHA: {commit_sha[:7]} by {developer_name} at {committed_at}")
            cursor.execute(query, (developer_name, commit_sha, commit_message, committed_at))
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
            (NOW() AT TIME ZONE 'UTC') - MAX(committed_at AT TIME ZONE 'UTC') AS time_since_last_commit,
            CASE
                WHEN NOW() AT TIME ZONE 'UTC' - (MAX(committed_at) AT TIME ZONE 'UTC') > INTERVAL '72 hours' THEN TRUE
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
            result = cursor.fetchone()

            if not result or result[0] is None:
                return {"hours_elapsed": 0, "breached": False, "empty_db": True}
            
            time_delta = result[0]
            hours_elapsed = int(time_delta.total_seconds() / 3600)

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

def commit_exists(commit_sha: str) -> bool:
    """Checks if a commit SHA already exists in the velocity_metrics table."""
    query = "SELECT 1 FROM velocity_metrics WHERE commit_sha = %s LIMIT 1;"
    connection = get_db_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (commit_sha,))
            return cursor.fetchnone() is not None
    except Exception as e:
        print(f"DAO Error checking commit existence: {e}")
        return False
    finally:
        connection.close()