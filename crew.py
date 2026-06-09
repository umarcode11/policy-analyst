import os
import litellm
litellm.drop_params = True
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import news_monitor, policy_analyst, verdict_writer
from tasks import create_tasks
from fallback.fallback_handler import with_fallback, validate_output
from langfuse import Langfuse

load_dotenv()

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

def run_policy_analysis(claim: str) -> str:

    def primary_run():
        tasks = create_tasks(claim)
        crew = Crew(
            agents=[news_monitor, policy_analyst, verdict_writer],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        result = crew.kickoff()
        return str(result)

    def fallback_run():
        print("[Fallback] Attempting simplified single-agent run...")
        from tools.search_tool import search_web
        from tools.custom_tool import score_claim_confidence
        search_result = search_web(claim)
        score_result = score_claim_confidence(claim, search_result)
        return (
            f"FALLBACK VERDICT REPORT\n"
            f"{'='*50}\n"
            f"CLAIM: {claim}\n\n"
            f"NOTE: Full multi-agent analysis unavailable. "
            f"Simplified fallback analysis used.\n\n"
            f"SEARCH FINDINGS:\n{search_result}\n\n"
            f"CONFIDENCE ASSESSMENT:\n{score_result}"
        )

    result = with_fallback(
        primary_func=primary_run,
        fallback_func=fallback_run,
        retries=2,
        delay=3
    )

    if not validate_output(result, min_length=50):
        result = "Analysis could not be completed. Please try again with a more specific claim."

    try:
        langfuse.create_event(
            name="policy-analysis-run",
            input={"claim": claim},
            output={"result": result[:500]}
        )
        langfuse.flush()
        print("[Langfuse] Event logged successfully.")
    except Exception as e:
        print(f"[Langfuse Warning] Could not log: {e}")

    return result 