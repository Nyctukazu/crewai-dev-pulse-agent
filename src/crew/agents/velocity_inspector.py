from crewai import Agent
import yaml
from src.tools.db_tool import save_commit_tool, save_figma_tool

with open('config/agents.yaml', 'r') as f:
    config = yaml.safe_load(f)['velocity_inspector_agent']

def get_velocity_inspector_agent(tools, target_llm): 
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        llm=target_llm,
        tools=[
            save_commit_tool, 
            save_figma_tool
        ],
        memory=False,
        cache=False,
        verbose=True
    )