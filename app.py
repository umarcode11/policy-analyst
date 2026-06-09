import gradio as gr
import threading
from crew import run_policy_analysis

def analyze_claim(claim: str):
    if not claim or len(claim.strip()) < 10:
        return "Please enter a valid policy claim or government statement (at least 10 characters)."

    print(f"\n[App] Analyzing claim: {claim}\n")

    result_container = []

    def run():
        try:
            result = run_policy_analysis(claim)
            result_container.append(result)
        except Exception as e:
            result_container.append(
                f"An error occurred while processing your request.\n"
                f"Error: {str(e)}\n\n"
                f"Please try again or rephrase your claim."
            )

    thread = threading.Thread(target=run)
    thread.start()
    thread.join(timeout=300)

    if result_container:
        return result_container[0]
    return "Request timed out. Please try again."


with gr.Blocks(title="Pakistan Policy Analyst") as app:

    gr.Markdown("""
    # Pakistan Policy Analyst
    ### AI-Powered Claim Verification and Policy Analysis

    Enter a government statement, policy claim, or news assertion below.
    The system will research, analyze, and deliver a structured verdict.

    Examples:
    - Pakistan's inflation has dropped to single digits under the current government
    - The government has successfully increased tax revenue by 30% this year
    - Pakistan has achieved energy self-sufficiency through new power projects
    """)

    with gr.Row():
        with gr.Column():
            claim_input = gr.Textbox(
                label="Policy Claim or Government Statement",
                placeholder="Enter a claim to verify...",
                lines=3
            )
            analyze_btn = gr.Button("Analyze Claim", variant="primary")

        with gr.Column():
            result_output = gr.Textbox(
                label="Verdict Report",
                lines=20
            )

    analyze_btn.click(
        fn=analyze_claim,
        inputs=claim_input,
        outputs=result_output
    )

    gr.Markdown("Powered by CrewAI | Groq LLaMA 3.3 70B | Langfuse Observability")

if __name__ == "__main__":
    app.launch() 