import os
import requests
from crewai.tools import tool

@tool("Figma File Activity Inspector")
def fetch_figma_activity(file_key: str) -> str:
    """Fetches recent version history updates from a specific Figma design file using the REST API."""
    token = os.getenv("FIGMA_TOKEN")
    if not token:
        return "Error: FIGMA_TOKEN missing from environment properties."
    
    url = f"https://api.figma.com/v1/files/{file_key}/comments"
    headers = {"X-Figma-Token": token}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Figma API Error: HTTP {response.status_code} - {response.text}"
        
        data = response.json()
        comments = data.get("comments", [])

        if not comments:
            return "No recent design versions or checkpoints detected in this Figma file."
        
        summary = []

        comments.sort(key=lambda x: x.get("created_at", ""), reverse=True)

        for c in comments[:10]:
            user = c.get("user", {}).get("handle", "Unknown Designer")
            message = c.get("message") or "Left a pin droplet markup."
            created_at = c.get("created_at")
            summary.append(f"- [{created_at}] {user} updated '{message}': Active feedback log.")

        return "\n".join(summary)
    
    except Exception as e:
        return f"System Failure connecting to Figma API: {str(e)}"