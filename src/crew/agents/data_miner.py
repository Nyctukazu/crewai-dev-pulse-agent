from crewai import Agent
from src.tools.figma_tool import fetch_figma_activity
from src.tools.github_tool import fetch_recent_commits
from src.tools.db_tool import save_commit_record, save_figma_record
import yaml

with open('config/agents.yaml', 'r') as f:
    config = yaml.safe_load(f)['data_miner_agent']


def get_data_miner_agent(tools, target_llm):
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        llm=target_llm,
        tools=[
            fetch_figma_activity,
            fetch_recent_commits
        ],
        memory=False,
        cache=False,
        verbose=True
    )