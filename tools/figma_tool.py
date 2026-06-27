import os
import requests
from crewai.tools import tool

@tool("Figma File Activity Inspector")
def fetch_figma_activity(file_key: str) -> str:
    """Fetches recent version history updates from a specific Figma design file using the REST API."""
    token = os.getenv("FIGMA_TOKEN")
    if not token:
        return "Error: FIGMA_TOKEN missing from environment properties."
    
    url = f"https://api.figma.com/v1/files/{file_key}/versions"
    headers = {"X-Figma-Token": token}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Figma API Error: HTTP {response.status_code} - {response.text}"
        
        data = response.json()
        versions = data.get("versions", [])

        if not versions:
            return "No recent design versions or checkpoints detected in this Figma file."
        
        summary = []
        for v in versions[:5]:
            label = v.get("label") or "Untitled Iteration"
            description = v.get("description") or "No description provided."
            user = v.get("user", {}).get("handle", "Unknown Designer")
            created_at = v.get("created_at")
            summary.append(f"- [{created_at}] {user} updated '{label}': {description}")

        return "\n".join(summary)
    
    except Exception as e:
        return f"System Failure connecting to Figma API: {str(e)}"