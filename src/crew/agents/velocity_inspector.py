from crewai import Agent
from src.tools.db_tool import team_status_tool
import yaml

with open('config/agents.yaml', 'r') as f:
    config = yaml.safe_load(f)['velocity_inspector_agent']

def get_velocity_inspector_agent(target_llm): 
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        llm=target_llm,
        tools=[
            team_status_tool
            ],
        memory=False,
        cache=False,
        verbose=True
    )
