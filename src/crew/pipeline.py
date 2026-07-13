from src.crew.agents_config import execute_crew_workflow, groq_llm, local_llm
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

    try:
        print("\n[Pipeline Core] Attempting primary execution via Cloud Engine (Groq)...")
        result = execute_crew_workflow(
            target_llm=groq_llm,
            inputs=inputs,
            is_fallback=False
        )
        return result
    
    except litellm.RateLimitError:
        print("\nPIPELINE ALERT: Cloud Infrastructure Rate Limit Triggered!")
        print("Hot-swapping model core to local on-premise hardware backup...")

        result = execute_crew_workflow(
            target_llm=local_llm,
            inputs=inputs,
            is_fallback=True
        )
        return result