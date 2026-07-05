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

def fetch_github_logs():
    """
    Retrieves all recorded git commits and design activities ordered by timestamp for dynamic graph rendering.
    """

    query = """
        SELECT 
            developer_name as person,
            committed_at as activity_time,
            'GitHub Commit' as activity_type,
            commit_message as detail
        FROM velocity_metrics
        ORDER BY activity_time DESC;
    """

    connection = get_db_connection()
    if not connection:
        return []
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"DAO Error fetching activity logs: {e}")
        return []
    finally:
        connection.close()

def fetch_figma_logs():
    """Retrives all Figma design metrics."""
    query = """
        SELECT
            designer_name as person,
            modified_at as activity_time,
            component_name as detail,
            action_type 
        FROM figma_metrics 
        ORDER BY modified_at DESC;
    """

    connection = get_db_connection()
    if not connection: return []
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"DAO Error fetching Figma logs: {e}")
        return []
    finally:
        connection.close()

def figma_event_exists(designer_name: str, modified_at: str) -> bool:
    """
    Checks if a specific design modification timestamp already exists for a designer.
    """
    query = """
        SELECT 1
        FROM figma_metrics
        WHERE designer_name = %s
        AND modified_at = %s
        LIMIT 1;
    """
    connection = get_db_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            cursor.execure(query, (designer_name, modified_at))
            return cursor.fetchnone() is not None
    except Exception as e:
        print(f"DAO Error checking Figma event: {e}")
        return False
    finally:
        connection.close()

def save_figma_record(designer_name: str, file_key: str, component_name: str, action_type: str, modified_at: str) -> bool:
    """
    Inserts a verified Figma asset event row into Neon.
    """

    query = """
        INSERT INTO figma_metrics (designer_name, file_key, component_name, action_type, modified_at)
        VALUES (%s, %s, %s, %s, %s);
    """

    connection = get_db_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (designer_name, file_key, component_name, action_type, modified_at))
            connection.commit()
            return True
    except Exception as e:
        print(f"DAO Error saving Figma record: {e}")
        return False
    finally:
        connection.close()