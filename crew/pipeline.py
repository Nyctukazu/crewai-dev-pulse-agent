import os
from crewai import Crew, Process
from crew.agents import execute_crew_workflow, groq_llm, local_llm
from crew.tasks import velocity_inspection_task, evaluate_figma_task
from tools.figma_tool import fetch_figma_activity
from crewai import Task
import litellm


def run_velocity_pipeline(repo_owner: str, repo_name: str, figma_file_key: str):
    """
    Orchestrates the orchestration pipeline with built-in High-Availability failover logic.
    """

    inputs = {
        "repo_owner": repo_owner,
        "repo_name": repo_name,
        "figma_file_key": figma_file_key
    }

    evaluate_design_task = Task(
        description=f"Inspect the recent design iterations for the Figma file key: '{figma_file_key}'.",
        expected_output="A summarized report of UI/UX updates detailing whether design assets match development output.",
        tools=[fetch_figma_activity]
    )

    pipeline_tasks = [velocity_inspection_task, evaluate_figma_task]

    try:
        print("\n[Pipeline Core] Attempting primary execution via Cloud Engine (Groq)...")
        result = execute_crew_workflow(
            target_llm=groq_llm,
            tasks=pipeline_tasks,
            inputs=inputs,
            is_fallback=False
        )
        return result
    
    except litellm.RateLimitError:
        print("\nPIPELINE ALERT: Cloud Infrastructure Rate Limit Triggered!")
        print("Hot-swapping model core to local on-premise hardware backup...")

        result = execute_crew_workflow(
            target_llm=local_llm,
            tasks=pipeline_tasks,
            inputs=inputs,
            is_fallback=True
        )
        return result