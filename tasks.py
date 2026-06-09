from crewai import Task
from agents import news_monitor, policy_analyst, verdict_writer


def create_tasks(claim: str):

    # Task 1: Research and collect news
    research_task = Task(
        description=(
            f"Research the following policy claim or government statement:\n\n"
            f"CLAIM: {claim}\n\n"
            f"Your job is to:\n"
            f"1. Search for recent news coverage about this claim\n"
            f"2. Find any official government statements or press releases\n"
            f"3. Identify what major Pakistani news sources are saying\n"
            f"4. Collect at least 3-5 relevant pieces of evidence\n"
            f"5. Note the dates and sources of all findings\n\n"
            f"Be thorough. Do not fabricate sources. Only report what you find."
        ),
        expected_output=(
            "A structured research summary containing:\n"
            "- The original claim\n"
            "- 3-5 evidence snippets with sources and dates\n"
            "- Key quotes or data points found\n"
            "- Any conflicting information discovered"
        ),
        agent=news_monitor
    )

    # Task 2: Analyze and score the claim
    analysis_task = Task(
        description=(
            f"Using the research collected, analyze the following claim:\n\n"
            f"CLAIM: {claim}\n\n"
            f"Your job is to:\n"
            f"1. Use the Claim Confidence Scorer tool to score the evidence\n"
            f"2. Identify whether the evidence supports or contradicts the claim\n"
            f"3. Note any gaps, missing data, or unverified assertions\n"
            f"4. Assess the credibility of the sources found\n"
            f"5. Produce a structured analysis with a confidence rating\n\n"
            f"Be critical and objective. Apply journalistic standards."
        ),
        expected_output=(
            "A structured analysis containing:\n"
            "- Confidence score (HIGH / MEDIUM / LOW / CONTRADICTED)\n"
            "- Evidence evaluation (what supports, what contradicts)\n"
            "- Source credibility assessment\n"
            "- Key gaps or missing information\n"
            "- Overall analytical verdict"
        ),
        agent=policy_analyst,
        context=[research_task]
    )

    # Task 3: Write the final verdict report
    verdict_task = Task(
        description=(
            f"Based on the research and analysis, write a final verdict report "
            f"for the following claim:\n\n"
            f"CLAIM: {claim}\n\n"
            f"Your report must include:\n"
            f"1. A clear headline summarizing the verdict\n"
            f"2. The original claim being assessed\n"
            f"3. A verdict label: VERIFIED / MISLEADING / UNVERIFIED / CONTRADICTED\n"
            f"4. Key evidence summary (2-3 sentences)\n"
            f"5. Confidence level and reasoning\n"
            f"6. Recommended follow-up questions or areas for further investigation\n\n"
            f"Write clearly and concisely. This report may be published or shared."
        ),
        expected_output=(
            "A complete verdict report with:\n"
            "- Headline\n"
            "- Original claim\n"
            "- Verdict label\n"
            "- Evidence summary\n"
            "- Confidence level\n"
            "- Follow-up recommendations\n"
            "- Word count: 200-400 words"
        ),
        agent=verdict_writer,
        context=[research_task, analysis_task]
    )

    return [research_task, analysis_task, verdict_task] 