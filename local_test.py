import os
import sys
from crewai import LLM, Crew, Process
import litellm


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

local_llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

print("Running suystem entirely on local machine hardware via Ollama...")

try:
    from crewai import Agent, Task

    local_inspector = Agent(
        role="E5 Velocity Inspector",
        goal="Inspect recent design iterations for Figma files locally",
        backstory="A local instance of the 35 developer tracking pipeline.",
        verbose=True,
        llm=local_llm,
        tools=[]
    )

    local_task = Task(
        description="Inspect the recent design iterations for the Figma file key: 's1sE1lI4ldL9Ms2SBv9YkO'.",
        expected_output="A structured summary of recent modifications.",
        agent=local_inspector
    )

    crew = Crew(
        agents=[local_inspector],
        tasks=[local_task],
        process=Process.sequential
    )

    result = crew.kickoff()
    print("Local run completed successfully!")
    print(result)

except Exception as e:
    print(f"Local execution failed: {e}")