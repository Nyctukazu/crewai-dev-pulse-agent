import os
import asyncio
from pathlib import Path
from typing import Any
from crewai import Agent, LLM
from crewai.tools import tool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
from tools.github_tool import fetch_recent_commits

project_root = Path(__file__).resolve().parents[1]
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

token_value = os.getenv("GITHUB_TOKEN") or "TEMPORARY_BLANK_TOKEN"

# os.environ["OPENAI_API_KEY"] = os.getenv("GROQ_API_KEY") 
# os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
# os.environ["OPENAI_MODEL_NAME"] = "groq/llama-3.3-70b-versatile"

groq_llm = LLM(
    model="openai/llama-3.3-70b-versatile",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2,
    extra_headers={
        "no-cache": "true"
    }
)

server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    env={
        "GITHUB_PERSONAL_ACCESS_TOKEN": token_value,
        **os.environ
    }
)

def run_mcp_tool_sync(tool_name: str, **kwargs) -> str:
    async def invoke_mcp():
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                res = await session.call_tool(tool_name, arguments=kwargs)
                return "".join([content.text for content in res.content if hasattr(content, "text")])
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        import nest_asyncio
        nest_asyncio.apply()
        return loop.run_until_complete(invoke_mcp())
    else:
        return asyncio.run(invoke_mcp())
    
def discover_and_bridge_mcp_tools():
    native_tools = []

    async def fetch_schemas():
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                return await session.list_tools()
    
    print("[System Init] Connecting to GitHub MCP Server process...")
    try: 
        mcp_data = asyncio.run(fetch_schemas())
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
        mcp_data = asyncio.get_event_loop().run_until_complete(fetch_schemas())

    for mcp_tool in mcp_data.tools:

        def make_executor(t_name=mcp_tool.name):
            return lambda **kwargs: run_mcp_tool_sync(t_name, **kwargs)

        @tool
        def dummy_mcp_bridge_tool(**kwargs) -> str:
            """Temporary placeholder docstring to satisfy CrewAI validation."""
            return ""

        dummy_mcp_bridge_tool.name = mcp_tool.name
        dummy_mcp_bridge_tool.description = mcp_tool.description or f"GitHub MCP tool: {mcp_tool.name}"
        dummy_mcp_bridge_tool._run = make_executor()

        native_tools.append(dummy_mcp_bridge_tool)

    return native_tools

github_tools = discover_and_bridge_mcp_tools()
print(f"[System Init] Successfully attached {len(github_tools)} GitHub tools to the agent runtime.")

velocity_inspector_agent = Agent(
    role="E5 Velocity Inspector",
    goal="Analyze repository commit frequencies to evaluate solo engineering consistency.",
    backstory="An automated auditing agent dedicated to extracting precise contribution frequencies.",
    llm=groq_llm,
    tools=[fetch_recent_commits],
    memory=False,
    cache=False,
    verbose=True
)