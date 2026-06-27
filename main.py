import sys
try:
    # Target the raw class where CrewAI compiles message formatting
    from crewai.agents.parser import AgentAction  
    import crewai.llms.cache as _crewai_cache
    _crewai_cache.mark_cache_breakpoint = lambda msg: msg
except (ImportError, AttributeError):
    pass

from dotenv import load_dotenv
from crew.pipeline import run_velocity_pipeline
from repository.velocity_dao import check_inactivity_status

def main():
    print("=" * 70)
    print("         E5 VELOCITY ENGINE - SYSTEM BOOTSTRAP INITIALIZED       ")
    print("=" * 70)

    load_dotenv()

    TARGET_REPO_OWNER = "Nyctukazu"
    TARGET_REPO_NAME = "crewai-dev-pulse-agent"
    TARGET_FIGMA_KEY = "s1sE1lI4ldL9Ms2SBv9YkO"

    if TARGET_REPO_OWNER == "your-github-username":
        print("[WARNING] You are using default placeholder string values.")
        print("Please update main.py parameters with your real developer profiles.\n")
        sys.exit(1)

    try:
        pipeline_output = run_velocity_pipeline(
            repo_owner=TARGET_REPO_OWNER,
            repo_name=TARGET_REPO_NAME,
            figma_file_key=TARGET_FIGMA_KEY
        )

        print("\n" + "-" * 50)
        print("AGENT PIPELINE ANALYSIS OUTPUT:")
        print("-" *50)
        print(pipeline_output)

        print("\n[Database Audit] Querying Neon persistence store for threshold tracking calculations...")
        db_status = check_inactivity_status()

        if db_status:
            print(f"-> Hours elapsed since last verifiable commit: {db_status['hours_elapsed']}h")
            if db_status['breached']:
                print("CRITICAL METRIC ALERT: 72-hour inactivity threshold breached!")
            else:
                print("System Operational Status: Metrics are running within stable timeline paremeters.")

        else:
            print("Failure: Could not safely query the Neon analytics engine.")
    except Exception as e:
        print(f"\n[Fatal Core Crash] Pipeline context terminated unexpectedly: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()