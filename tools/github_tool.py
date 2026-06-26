import os
import requests
from datetime import datetime, timedelta, timezone
from crewai.tools import tool

@tool("Github Commit Fetcher")
def fetch_recent_commits(repo_owner: str, repo_name: str) -> str:
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "X-Github-Api-Version": "2022-11-28"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    three_days_ago = (datetime.now(timezone.utc) - timedelta(hours=72)).isoformat()

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    params = {
        "since": three_days_ago,
        "per_page": 100
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            return f"API Error: HTTP P{response.status_code} - {response.text}"
        commits_data = response.json()

        if not commits_data:
            return "ALERT: No commits found in the last 72 hours.  Inactivity theshold triggered."
        
        result = []
        for commit in commits_data:
            author = commit['commit']['author']['name']
            date = commit['commit']['author']['date']
            message = commit['commit']['message'].replace('\n', ' ')
            result.append(f"- [{date}] {author}: {message}")

        return "\n".join(result)
    
    except Exception as e:
        return f"System Failure connecting to Github API: {str(e)}"