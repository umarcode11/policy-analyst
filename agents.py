import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from crewai.tools import BaseTool
from crewai_tools import SerperDevTool

load_dotenv()

from tools.news_tool import get_pakistan_news
from tools.custom_tool import score_claim_confidence

groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
   
)

web_search_tool = SerperDevTool()

class PakistanNewsTool(BaseTool):
    name: str = "Pakistan News Tool"
    description: str = "Fetch recent Pakistan-related news about a policy or government claim."
    def _run(self, topic: str) -> str:
        return get_pakistan_news(topic)

class ClaimScorerTool(BaseTool):
    name: str = "Claim Confidence Scorer"
    description: str = "Score how well evidence supports or contradicts a policy claim. Input format: claim|||evidence"
    def _run(self, input_str: str) -> str:
        if "|||" in input_str:
            parts = input_str.split("|||", 1)
            claim = parts[0].strip()
            evidence = parts[1].strip()
        else:
            claim = input_str
            evidence = input_str
        return score_claim_confidence(claim, evidence)

pakistan_news_tool = PakistanNewsTool()
claim_scorer_tool = ClaimScorerTool()

news_monitor = Agent(
    role="Pakistan News Monitor",
    goal="Find and collect recent news coverage and public statements related to the given policy claim or government statement.",
    backstory="You are a seasoned media monitor with 15 years of experience tracking Pakistani government announcements, press releases, and news coverage. You know where to look, which sources matter, and how to quickly gather relevant information on any policy topic. You are thorough, fast, and factual.",
    llm=groq_llm,
    tools=[web_search_tool, pakistan_news_tool],
    verbose=True,
    allow_delegation=False
)

policy_analyst = Agent(
    role="Policy Analyst",
    goal="Analyze the collected evidence and evaluate whether it supports, contradicts, or is inconclusive about the given policy claim.",
    backstory="You are a rigorous policy analyst with expertise in Pakistani governance, economic policy, and public accountability. You have worked with think tanks and investigative journalism organizations. You evaluate claims critically, weigh evidence carefully, and never accept statements at face value.",
    llm=groq_llm,
    tools=[claim_scorer_tool, web_search_tool],
    verbose=True,
    allow_delegation=False
)

verdict_writer = Agent(
    role="Investigative Verdict Writer",
    goal="Produce a clear, structured verdict report based on the analysis, suitable for publication or briefing.",
    backstory="You are an experienced investigative journalist and editor who specializes in translating complex policy analysis into clear, readable verdicts. Your writing is direct, evidence-based, and accountable.",
    llm=groq_llm,
    tools=[web_search_tool],
    verbose=True,
    allow_delegation=False
)   