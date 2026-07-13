import os
import requests
from crewai.tools import tool

@tool("send_chat_notification")
def send_discord_notification(message: str) -> str:
    """
    Transmits a formatted markdown text payload directly to the team's dedicated Discord channel.
    Input should be a clean summary string of project health and inactivity gaps.
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        return "Error: DISCORD_WEBHOOK_URL environment variable is missing."
    
    payload = {
        "content": message
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 204:
            return "Successfully transmitted project velocity metrics report to Discord."
        else:
            return f"Failed to send notification.  Discord API status code: {response.status_code}"
        
    except Exception as e:
        return f"Network exception encountered while pushing to Discord: {str(e)}"