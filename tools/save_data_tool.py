from crewai.tools import tool
from repository.velocity_dao import save_commit_record

@tool("Save Commit to Database")
def save_commit_tool(developer_name: str, commit_sha: str, commit_message: str, committed_at: str) -> str:
    """Saves a single verified git commit record into the Neon persistent metrics store."""
    success = save_commit_record(developer_name, commit_sha, commit_message, committed_at)
    if success:
        return "Successfully archived commit record in the database."
    return "Failed to save record due to database error."