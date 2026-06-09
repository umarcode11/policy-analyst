## Demo Video
https://www.loom.com/share/89b1b931b78b4d4a8540c435de0ba730 

\# Policy Analyst — AI-Powered Claim Verification System



A multi-agent AI application built with CrewAI that researches, analyzes, and delivers structured verdicts on Pakistani government policy claims and public statements.



\## What It Does



You enter a government claim or policy statement. Three AI agents collaborate to:

1\. Search for recent news coverage and evidence

2\. Analyze and score the evidence against the claim

3\. Produce a structured verdict report with confidence level and follow-up recommendations





\## Project Structure



policy-analyst/

├── app.py                  # Gradio UI and entry point

├── crew.py                 # Crew assembly, execution, fallback, Langfuse logging

├── agents.py               # Three CrewAI agents with roles and tools

├── tasks.py                # Three tasks with descriptions and expected outputs

├── tools/

│   ├── custom\_tool.py      # Custom claim confidence scorer (built from scratch)

│   ├── search\_tool.py      # Serper web search wrapper

│   └── news\_tool.py        # Pakistan-focused news search

├── fallback/

│   └── fallback\_handler.py # Retry logic and graceful degradation

├── monitoring/

│   └── langfuse\_config.py  # Langfuse observability configuration

├── data/                   # Sample inputs

├── outputs/                # Sample outputs

├── requirements.txt

├── .env.example

└── README.md



\## Agents



\### 1. Pakistan News Monitor

\- \*\*Role:\*\* Finds and collects recent news coverage related to the claim

\- \*\*Tools:\*\* Web Search Tool, Pakistan News Tool

\- \*\*Output:\*\* Research summary with sources and dates



\### 2. Policy Analyst

\- \*\*Role:\*\* Evaluates evidence against the claim using structured scoring

\- \*\*Tools:\*\* Claim Confidence Scorer, Web Search Tool

\- \*\*Output:\*\* Analysis with confidence rating and evidence evaluation



\### 3. Investigative Verdict Writer

\- \*\*Role:\*\* Produces a clear, publishable verdict report

\- \*\*Tools:\*\* Web Search Tool

\- \*\*Output:\*\* Structured verdict with headline, label, evidence summary, and recommendations



\## Tools



\### Web Search Tool (SerperDevTool)

Built-in CrewAI tool using the Serper API to search Google. Returns top 5 results with titles, snippets, and sources.



\### Pakistan News Tool (Custom)

Queries the Serper news endpoint with "Pakistan" appended to every query. Focuses results on Pakistani sources like Dawn, Tribune, Geo, and Reuters Pakistan.



\### Claim Confidence Scorer (Custom-built)

Fully custom Python tool that takes a claim and evidence text, counts supporting, contradicting, and uncertain signals, and returns a score: HIGH CONFIDENCE, MEDIUM CONFIDENCE, LOW CONFIDENCE, or CONTRADICTED. No external API — pure logic.



\## Workflow



Sequential process:

User Input → News Monitor → Policy Analyst → Verdict Writer → Output



Each agent receives the output of the previous agent as context via the `context` parameter in tasks.



\## Fallback Mechanism



If the main crew fails:

1\. Retries up to 2 times with a 3-second delay

2\. If still failing, runs a simplified backup analysis using only the search tool and custom scorer directly

3\. Returns a clearly labelled FALLBACK VERDICT REPORT

4\. Never crashes — always returns a response



Tested failure scenario: LLM API errors trigger fallback automatically.



\## Langfuse Observability



Every run is logged to Langfuse with:

\- Input claim

\- Output verdict (first 500 characters)

\- Timestamp

\- Event name: policy-analysis-run



View traces at: https://cloud.langfuse.com



\## MCP Awareness



This project does not implement MCP but would benefit significantly from it in the following ways:



\*\*What could be exposed through MCP:\*\*

\- Dawn, Geo, ARY RSS news feeds as live MCP data sources

\- SECP (Securities and Exchange Commission Pakistan) company registry as an MCP tool

\- Federal Board of Revenue (FBR) tax data as an MCP data source

\- National Assembly bill tracker as an MCP resource

\- Pakistan Bureau of Statistics economic indicators as an MCP feed



\*\*How MCP would help:\*\*

\- Tool integration would become standardized — each data source exposes a consistent interface

\- Agents could connect to any MCP server without custom code per source

\- New data sources could be added without modifying agent code

\- The Claim Confidence Scorer could be exposed as an MCP tool for other applications to use



\*\*Which parts would benefit most:\*\*

The News Monitor agent currently relies on general web search. With MCP servers for Dawn, Tribune, and official government portals, it would retrieve authoritative Pakistani sources directly rather than hoping Google surfaces them.



\## Setup Instructions



\### 1. Clone the repository

```bash

git clone https://github.com/umarcode11/policy-analyst.git

cd policy-analyst

```



\### 2. Create conda environment

```bash

conda create -n policy-analyst python=3.11

conda activate policy-analyst

```



\### 3. Install dependencies

```bash

pip install -r requirements.txt

pip install litellm

```



\### 4. Set up environment variables

Copy `.env.example` to `.env` and fill in your keys:

```bash

cp .env.example .env

```



\### 5. Run the application

```bash

python app.py

```



Open your browser at `http://127.0.0.1:7860`



\## API Keys Required



| Key | Where to get it |

|---|---|

| GROQ\_API\_KEY | console.groq.com |

| SERPER\_API\_KEY | serper.dev |

| LANGFUSE\_SECRET\_KEY | cloud.langfuse.com |

| LANGFUSE\_PUBLIC\_KEY | cloud.langfuse.com |

| LANGFUSE\_HOST | https://cloud.langfuse.com |



\## Example Claims to Test



\- "Pakistan's inflation has dropped to single digits under the current government"

\- "The government has successfully increased tax revenue by 30% this year"

\- "Pakistan has achieved energy self-sufficiency through new power projects"

\- "The rupee has stabilized due to government economic reforms"



\## Tech Stack



\- CrewAI 1.14.6

\- Groq LLaMA 3.3 70B

\- Langfuse 4.7.1

\- Gradio 5.x

\- Serper API

\- Python 3.11 



