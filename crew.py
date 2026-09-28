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
# Keep text small
# ---------------------------------------------------------
def trim_text(text, max_chars=3500):
    if not text:
        return ""

    text = str(text)

    if len(text) <= max_chars:
        return text

    return (
        text[:max_chars]
        + "\n\n[Content shortened to control token usage.]"
    )


# ---------------------------------------------------------
# Wait after rate limit
# ---------------------------------------------------------
def wait_for_rate_limit(error_text):
    match = re.search(
        r"try again in ([0-9]+(?:\.[0-9]+)?)s",
        str(error_text),
        re.IGNORECASE,
    )

    if match:
        seconds = float(match.group(1))
        wait_seconds = max(10, seconds + 5)
    else:
        wait_seconds = 20

    print(
        f"Groq rate limit reached. "
        f"Waiting {wait_seconds:.1f} seconds..."
    )

    time.sleep(wait_seconds)


# ---------------------------------------------------------
# Run one agent
# ---------------------------------------------------------
def run_single(
    agent,
    description,
    expected_output,
    max_iterations=1,
):
    """
    Run one CrewAI agent.

    Non-tool agents use 1 iteration.
    Tool-using agents can use 2 iterations.
    """

    try:
        agent.max_iter = max_iterations
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

    # Small delay between agents
    time.sleep(10)

    max_attempts = 2

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

            else:
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

    question = trim_text(question, 1500)

    if depth == "Quick":

        source_limit = (
            "Use only the most important sources. "
            "Keep everything concise."
        )

    elif depth == "Deep":

        source_limit = (
            "Use several important sources, "
            "but keep the output concise."
        )

    else:

        source_limit = (
            "Use a balanced number of high-quality sources."
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
Research question:

{question}

Depth:
{depth}

Create a SHORT research plan.

Identify:
- main sub-questions
- evidence needed
- preferred source types
- important verification points

{source_limit}

Do not write the final report.
Keep the answer under 500 words.
""",
        "A short research plan.",
        max_iterations=1,
    )

    plan = trim_text(plan, 2500)

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

Research plan:

{plan}

Use your Live Web Search tool.

Find the most useful authoritative sources.

Prefer:
- official organizations
- universities
- original research
- standards bodies
- official technical documentation

For each important source provide:
- title
- URL
- short evidence note

Do not invent URLs.

{source_limit}

Keep the research dossier SHORT.
Maximum about 700 words.
""",
        "A short source-backed research dossier.",
        max_iterations=2,
    )

    research = trim_text(research, 4000)

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

Use your Web Page Reader tool.

Check only the most important sources.

For each important source identify:
- whether it supports the claim
- important evidence
- publication date if available
- source authority
- important limitation

Keep the analysis SHORT.
Do not repeat the entire research dossier.
""",
        "A short source-analysis report.",
        max_iterations=2,
    )

    source_analysis = trim_text(source_analysis, 3500)

    if on_agent_done:
        on_agent_done(2)

    # =====================================================
    # 4. FACT CHECKER
    # =====================================================

    if on_agent_start:
        on_agent_start(3, AGENT_NAMES[3])

    checker = create_fact_checker()

    # IMPORTANT:
    # The Fact Checker now checks the evidence we already collected.
    # It does NOT need another web-search cycle.
    fact_check = run_single(
        checker,
        f"""
Fact-check the following research material.

Research question:

{question}

Research:

{research}

Source analysis:

{source_analysis}

Identify only:

- supported claims
- questionable claims
- conflicting information
- missing evidence
- important limitations

Use ONLY the supplied research and source analysis.

Do not perform additional web searches.

Keep the fact-checking memo SHORT.
Maximum about 500 words.
""",
        "A short fact-checking memo.",
        max_iterations=1,
    )

    fact_check = trim_text(fact_check, 3000)

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

Question:

{question}

Research:

{research}

Source analysis:

{source_analysis}

Fact-check:

{fact_check}

Create these sections:

1. Executive Summary
2. Key Findings
3. Detailed Analysis
4. Evidence & Sources
5. Uncertainty / Conflicts
6. Limitations
7. Conclusion
8. Sources

Keep the report concise.

Use only information supplied above.

Do not invent URLs.

Clearly identify uncertainty.
""",
        "A concise final research report with sources.",
        max_iterations=1,
    )

    report = trim_text(report, 9000)

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

            if url.startswith(
                ("http://", "https://")
            ):

                if url not in seen:

                    seen.add(url)

                    sources.append(
                        {
                            "title": "Research source",
                            "url": url,
                        }
                    )

    return sources[:8]
