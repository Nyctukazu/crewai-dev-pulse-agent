from crewai import Task

extract_git_metrics_task = Task(
    description=(
        "1. Use the official GitHub MCP server tools or fetch_recent_commits to investigate the commit history "
        "of the target repository: '{repo_owner}/{repo_name}'.\n"
        "2. For EVERY commit you find, read its SHA, author, message, and date.\n"
        "3. Immediately invoke the 'Save Commit to Database' tool for each individual commit to archive it.\n"
        "4. Stop if the tool returns a 'Skip' message indicating older records have been reached."
    ),
    expected_output="A structured summary reporting how many new commits were successfully archived versus skipped."
)

evaluate_velocity_gaps_task = Task(
    description=(
        "Analyze the structure data extracted from the previous task.  Verify if "
        "the latest commit activity timestamps fall safely within the required timeline, "
        "or if there is an operational gap creeping toward the maximum 72-hour threshold limit."

    ),
    expected_output=(
        "A summarizing performance log detailing total active commit counts and highlighting "
        "the exact hours elapsed since the last verifiable push event."
    )
)

velocity_inspection_task = Task(
    description=(
        "Investigate the commit history of the target repository. "
        "You MUST use the 'Github Commit Fetcher' tool for this task. "
        "Provide it with these exact arguments:\n"
        "  - repo_owner: '{repo_owner}'\n"
        "  - repo_name: '{repo_name}'\n\n"
        "Analyze the output string to identify the commit SHAs, the author's name, "
        "the exact timestamps, and the messages."
    ),
    expected_output="A structured summary of recent commit metrics and timelines.",
)