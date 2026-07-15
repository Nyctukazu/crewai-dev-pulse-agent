from crewai.tools import tool
from src.repository.velocity_dao import save_commit_record, commit_exists, figma_event_exists, save_figma_record, get_developers_status

@tool("Save Commit to Database")
def save_commit_tool(developer_name: str, commit_sha: str, commit_message: str, committed_at: str) -> str:
    """Saves a single verified git commit record into the Neon persistent metrics store."""
    if commit_exists(commit_sha):
        return f"Skip: Commit {commit_sha[:7]} is already archived.  Do not insert duplicates."
    
    success = save_commit_record(developer_name, commit_sha, commit_message, committed_at)
    if success:
        return "Successfully archived commit record in the database."
    return "Failed to save record due to database error."

@tool("Save Figma Activity to Database")
def save_figma_tool(designer_name: str, file_key: str, component_name: str, action_type: str, modified_at: str) -> str:
    """Saves a verified Figma design update or component modification event into the Neon database."""

    if figma_event_exists(designer_name, modified_at):
        return f"Skip: Design event by {designer_name} at {modified_at} is already archived."
    
    success = save_figma_record(designer_name, file_key, component_name, action_type, modified_at)
    if success:
        return f"Successfully archived new Figma asset metric for {designer_name}."
    return "Failed to log design event due to a database backend error."

@tool("Get Project Team Status")
def get_project_team_status() -> str:
    """
    Queries the PostgreSQL database and returns the deterministic
    activity status, inactive hours, and daily contribution markers
    for all team contributors.
    """

    statuses = get_developers_status()
    if not statuses:
        return "No contributor metrics found in the database."
    
    output = []
    for member in statuses:
        alert_flag = "BREACH" if member['status'] == "INACTIVE" else "OK"
        output.append(
            f"- **{member['name']}**: Status is {member['status']} ({alert_flag})."
            f"Last active: {member['hours_inactive']} hours ago. "
            f"Contributed today: {member['has_contributed_today']}"
        )
    return "\n".join(output)