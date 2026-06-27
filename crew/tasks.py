from crewai import Task
from crew.agents import velocity_inspector_agent

extract_git_metrics_task = Task(
    description=(
        "Use the official GitHub MCP server tools to investigate the commit history "
        "of the target repository: '{repo_owner}/{repo_name}'. "
        "Identify the commit SHA, the author's name, the exact timestamp of the commit, "
        "and the commit message text.  Focus specifically on isolating contributions made "
        "by the developer over the current execution boundary timelin."
    ),
    expected_output=(
        "A structure JSON-formatted list of dictionaties containing individual commit profiles. "
        "Example structure: [{{'sha': '...', 'author': '...', 'date': '...', 'message': '...'}}]"
    ),
    agent=velocity_inspector_agent
)

evaluate_velocity_gaps_task = Task(
    description=(
        "Analyze the structure data extracted from the previous task.  Verify if "
        "the latest commit activity timestamps fall safely withint the required timeline, "
        "or if there is an operational gap creeping toward the maximum 72-hour threshold limit."

    ),
    expected_output=(
        "A summarizing performance log detailing total active commit counts and highlighting "
        "the exact hours elapsed since the last verifiable push event."
    ),
    agent=velocity_inspector_agent
)