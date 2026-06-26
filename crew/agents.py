import os
from crewai import Agent
from mcp import StdioServerParameters

github_mcp_config = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    env={
        "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN"),
        **os.environ
    }
)

velocity_inspector_agent = Agent(
    role="E5 Velocity Inspector",
    goal="Analyze repository commit frequencies to evaluate solo engineering consistency.",
    backstory="An automated auditing agent dedicated to extracting precise contribution frequencies.",
    tools=[github_mcp_config],
    verbose=True
)