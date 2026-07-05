from crewai import Task

velocity_inspection_task = Task(
    description=(
        "1. Fetch recent repository history by running the 'Github Commit Fetcher' tool.\n"
        "   Pass these exact inputs: repo_owner: '{repo_owner}', repo_name: '{repo_name}'.\n"
        "2. Parse the output lines carefully to extract the unique SHA signature, author name, timestamp, and commit message.\n"
        "3. For EVERY single commit line found in the log, you MUST immediately call the 'Save Commit to Database' tool.\n"
        "   Map the variables carefully: pass the author's name to 'developer_name', the unique SHA to 'commit_sha', "
        "the raw message to 'commit_message', and the timestamp to 'committed_at'.\n"
        "4. Loop through and execute this save action for each item. Do not summarize or skip any commits."
    ),
    expected_output="A strict confirmation detailing exactly how many commit entries were processed and archived in Neon.",
)

evaluate_figma_task = Task(
    description=(
        "1. Fetch the recent design communication feed by running the 'Figma File Activity Inspector' tool.\n"
        "   Pass this exact input: file_key: '{figma_file_key}'.\n"
        "2. Read the output log lines carefully. Each line contains a designer name, a message/comment text, and a timestamp.\n"
        "3. For EVERY single design log line discovered, you MUST immediately call the 'Save Figma Activity to Database' tool.\n"
        "   Map the variables carefully: pass the designer's name to 'designer_name', the file key to 'file_key', "
        "the comment message string to 'label', and the timestamp to 'modified_at'.\n"
        "4. Loop through and execute this save action for each item. Do not skip any rows or stop prematurely."
    ),
    expected_output="A strict confirmation detailing exactly how many design entries were processed and sent to the database.",
)