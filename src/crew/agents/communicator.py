from crewai import Agent
from src.tools.discord_tool import send_discord_notification
import yaml

with open('config/agents.yaml', 'r') as f:
    config = yaml.safe_load(f)['communicator_agent']

def get_communicator_agent(target_llm):
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        llm=target_llm,
        tools=[
            send_discord_notification
        ],
        memory=False,
        cache=False,
        verbose=True
    )

