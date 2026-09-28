import re
import time

from crewai import Crew, Process, Task

from research_manager import create_agent as create_manager
from web_researcher import create_agent as create_researcher
from source_analyst import create_agent as create_source_analyst
from fact_checker import create_agent as create_fact_checker
from report_writer import create_agent as create_report_writer


AGENT_NAMES = [
    "Research Manager",
    "Web Researcher",
    "Source Analyst",
    "Fact Checker",
    "Report Writer",
]


# ---------------------------------------------------------
# Keep agent-to-agent context small
# ---------------------------------------------------------
def trim_text(text, max_chars=6000):
    if not text:
        return ""

    text = str(text)

    if len(text) <= max_chars:
        return text

    return (
        text[:max_chars]
        + "\n\n[Additional content was shortened to control token usage.]"
    )


# ---------------------------------------------------------
# Wait for Groq rate limits
# ---------------------------------------------------------
def wait_for_rate_limit(error_text):
    match = re.search(
        r"try again in ([0-9]+(?:\.[0-9]+)?)s",
        str(error_text),
        re.IGNORECASE,
    )

    if match:
        seconds = float(match.group(1))
        wait_seconds = max(5, seconds + 2)
    else:
        wait_seconds = 20

    print(f"Groq rate limit reached. Waiting {wait_seconds:.1f} seconds...")
    time.sleep(wait_seconds)


# ---------------------------------------------------------
# Run one agent
# ---------------------------------------------------------
def run_single(agent, description, expected_output):

    # Limit agent iterations so one agent cannot generate
    # many unnecessary LLM calls.
    try:
        agent.max_iter = 2
    except Exception:
        pass

    task = Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
        memory=False,
    )

    # Give Groq some breathing room between agents.
    time.sleep(8)

    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            return str(crew.kickoff())

        except Exception as e:
            error_text = str(e)

            if (
                "RateLimitError" in error_text
                or "rate_limit_exceeded" in error_text
                or "tokens per minute" in error_text
            ):
                if attempt == max_attempts - 1:
                    raise

                wait_for_rate_limit(error_text)
                continue

            raise

    raise RuntimeError("Agent execution failed.")


# ---------------------------------------------------------
# Main research workflow
# ---------------------------------------------------------
def run_research(
    question,
    depth="Standard",
    on_agent_start=None,
    on_agent_done=None,
):

    if depth == "Quick":
        source_limit = (
            "Use only a compact set of the most useful sources."
        )

    elif depth == "Deep":
        source_limit = (
            "Use a broader set of sources, but remain concise."
        )

    else:
        source_limit = (
            "Use a balanced set of high-quality sources."
        )

    # =====================================================
    # 1. RESEARCH MANAGER
    # =====================================================

    if on_agent_start:
        on_agent_start(0, AGENT_NAMES[0])

    manager = create_manager()

    plan = run_single(
        manager,
        f"""
User research question:

{question}

Research depth:

{depth}

Create a concise research plan.

Identify:
- major sub-questions
- evidence requirements
- preferred source types
- important verification points

{source_limit}

Do not write the final report.
Keep the plan concise.
""",
        "A concise research plan.",
    )

    plan = trim_text(plan, 4000)

    if on_agent_done:
        on_agent_done(0)

    # =====================================================
    # 2. WEB RESEARCHER
    # =====================================================

    if on_agent_start:
        on_agent_start(1, AGENT_NAMES[1])

    researcher = create_researcher()

    research = run_single(
        researcher,
        f"""
Research question:

{question}

Research manager plan:

{plan}

Use your Live Web Search tool.

Actually perform web searches.

Prioritize:
- official organizations
- original research
- universities
- standards bodies
- reputable technical documentation
- authoritative sources

Return:
- source title
- URL
- date when available
- concise evidence notes

{source_limit}

Do not invent URLs or facts.

Keep the research dossier concise.
""",
        "A concise source-backed research dossier with useful URLs.",
    )

    research = trim_text(research, 6500)

    if on_agent_done:
        on_agent_done(1)

    # =====================================================
    # 3. SOURCE ANALYST
    # =====================================================

    if on_agent_start:
        on_agent_start(2, AGENT_NAMES[2])

    analyst = create_source_analyst()

    source_analysis = run_single(
        analyst,
        f"""
Research question:

{question}

Research dossier:

{research}

Use your Web Page Reader tool on the most important URLs.

Check the actual pages.

Extract concise evidence about:
- publication date
- relevant evidence
- source authority
- context
- limitations
- important discrepancies

Focus only on the most important sources.

Keep the analysis concise.
""",
        "A concise source-analysis dossier.",
    )

    source_analysis = trim_text(source_analysis, 6000)

    if on_agent_done:
        on_agent_done(2)

    # =====================================================
    # 4. FACT CHECKER
    # =====================================================

    if on_agent_start:
        on_agent_start(3, AGENT_NAMES[3])

    checker = create_fact_checker()

    fact_check = run_single(
        checker,
        f"""
Research question:

{question}

Original research:

{research}

Source analysis:

{source_analysis}

Use Live Web Search to independently verify the most important
or uncertain claims.

Identify:

- supported claims
- unsupported claims
- conflicting claims
- outdated information
- important gaps

Do not invent evidence.

Keep the fact-checking memo concise.
""",
        "A concise fact-checking memo.",
    )

    fact_check = trim_text(fact_check, 5000)

    if on_agent_done:
        on_agent_done(3)

    # =====================================================
    # 5. REPORT WRITER
    # =====================================================

    if on_agent_start:
        on_agent_start(4, AGENT_NAMES[4])

    writer = create_report_writer()

    report = run_single(
        writer,
        f"""
Write the final research report.

Research question:

{question}

Research plan:

{plan}

Web research:

{research}

Source analysis:

{source_analysis}

Fact-checking memo:

{fact_check}

Create a concise but polished report with:

1. Executive Summary
2. Key Findings
3. Detailed Analysis
4. Evidence & Source Notes
5. Conflicting or Uncertain Information
6. Limitations
7. Conclusion
8. Sources

Keep the report focused.

Facts must be traceable to the supplied URLs.

Do not create URLs that were not supplied.

Clearly label uncertainty.
Do not present speculation as fact.
""",
        "A concise polished research report with sources.",
    )

    report = trim_text(report, 12000)

    if on_agent_done:
        on_agent_done(4)

    return {
        "report": report,
        "sources": extract_sources(research),
    }


# ---------------------------------------------------------
# Extract URLs
# ---------------------------------------------------------
def extract_sources(text):

    sources = []
    seen = set()

    for line in str(text).splitlines():

        if line.strip().lower().startswith("url:"):

            url = line.split(":", 1)[1].strip()

            if (
                url.startswith("http://")
                or url.startswith("https://")
            ):

                if url not in seen:
                    seen.add(url)

                    sources.append(
                        {
                            "title": "Research source",
                            "url": url,
                        }
                    )

    return sources[:10]
