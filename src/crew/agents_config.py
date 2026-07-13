import os
import sys
import asyncio
from pathlib import Path
from typing import Any
from crewai import LLM, Crew, Process
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
from agents.data_miner import get_data_miner_agent
from agents.velocity_inspector import get_velocity_inspector_agent
from tasks.tasks import velocity_inspection_task
import litellm

project_root = Path(__file__).resolve().parents[1]
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

token_value = os.getenv("GITHUB_TOKEN") or "TEMPORARY_BLANK_TOKEN"

groq_llm = LLM(
    model="openai/llama-3.3-70b-versatile",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2,
    extra_headers={
        "no-cache": "true"
    }
)

local_llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
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

def execute_crew_workflow(target_llm: LLM, tasks: list, inputs: dict, is_fallback=False):
    if is_fallback:
        print("\nSYSTEM NOTICE: Booting E5 Velocity Inspector on Local Compute (Ollama)...")
    else:
        print("\nSYSTEM NOTICE: Booting E5 Velocity Inspector on Cloud Engine (Groq)...")

    github_tools = [...]
    miner_agent = get_data_miner_agent(target_llm)
    velocity_tasks = velocity_inspection_task(miner_agent)
    inspector_agent = get_velocity_inspector_agent(target_llm)

    crew = Crew(
        agents=[miner_agent],
        tasks=[velocity_tasks],
        process=Process.sequential,
        verbose=True
    )

    return crew.kickoff(inputs=inputs)

if __name__ == "__main__":
    try:
        final_output = execute_crew_workflow(groq_llm, is_fallback=False)
        print("Analysis Complete via Cloud Engine.")
        print(final_output)
    
    except litellm.RateLimitError:
        print("\nCRITICAL ERROR: Cloud Infrastructure Rate Limit Triggered!")
        print("Hot-swapping model core to local on-premise hardware backup...")
        
        final_output = execute_crew_workflow(local_llm, is_fallback=True)
        print("Analysis Successfully Recovered and Completed via Local Machine Hardware.")
        print(final_output)

__all__ = ['execute_crew_workflow', 'groq_llm', 'local_llm']