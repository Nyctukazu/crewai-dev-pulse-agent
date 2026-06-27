import os
from crewai import Crew, Process
from crew.agents import velocity_inspector_agent
from crew.tasks import extract_git_metrics_task, evaluate_velocity_gaps_task
from tools.figma_tool import fetch_figma_activity
from crewai import Task

def run_velocity_pipeline(repo_owner: str, repo_name: str, figma_file_key: str):
    """
    Assembles the Crew runtime instance and executes the agent pipeline synchronously.
    """

    evaluate_design_task = Task(
        description=f"Inspect the recent design iterations for the Figma file key: '{figma_file_key}'.",
        expected_output="A summarized report of UI/UX updates detailing whether design assets match development output.",
        agent=velocity_inspector_agent,
        tools=[fetch_figma_activity]
    )

    velocity_crew = Crew(
        agents=[velocity_inspector_agent],
        tasks=[extract_git_metrics_task, evaluate_design_task, evaluate_velocity_gaps_task],
        process=Process.sequential,
        verbose=True
    )

    inputs = {
        "repo_owner": repo_owner,
        "repo_name": repo_name
    }

    print("\n[Engine Initialization] Firing up the CrewAI + Groq tracking worker...\n")
    result = velocity_crew.kickoff(inputs=inputs)
    return result