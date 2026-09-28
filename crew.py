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
# Keep context VERY small
# ---------------------------------------------------------
def trim_text(text, max_chars=2000):
    if not text:
        return ""

    text = str(text)

    if len(text) <= max_chars:
        return text

    return (
        text[:max_chars]
        + "\n\n[Content shortened.]"
    )


# ---------------------------------------------------------
# Wait for Groq rate limit
# ---------------------------------------------------------
def wait_for_rate_limit(error_text):

    match = re.search(
        r"try again in ([0-9]+(?:\.[0-9]+)?)s",
        str(error_text),
        re.IGNORECASE,
    )

    if match:
        seconds = float(match.group(1))
        wait_seconds = max(15, seconds + 5)
    else:
        wait_seconds = 30

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

    time.sleep(12)

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
                or "Request too large" in error_text
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

    question = trim_text(question, 1000)

    if depth == "Quick":

        source_limit = (
            "Use only the most important sources."
        )

    elif depth == "Deep":

        source_limit = (
            "Use several important sources, but stay concise."
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
Question:
{question}

Depth:
{depth}

Create a short research plan.

Identify:
- main questions
- evidence needed
- source types
- verification points

{source_limit}

Maximum 300 words.
""",
        "A short research plan.",
        max_iterations=1,
    )

    plan = trim_text(plan, 1500)

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
Question:
{question}

Research plan:
{plan}

Use your Live Web Search tool.

Find the most useful authoritative sources.

Return only:
- source title
- URL
- short evidence note

Prefer official organizations, universities,
research papers and technical documentation.

Do not invent URLs.

Maximum 500 words.
""",
        "A short research dossier with URLs.",
        max_iterations=2,
    )

    research = trim_text(research, 2500)

    if on_agent_done:
        on_agent_done(1)

    # =====================================================
    # 3. SOURCE ANALYST
    # =====================================================

    if on_agent_start:
        on_agent_start(2, AGENT_NAMES[2])

    analyst = create_source_analyst()

    # IMPORTANT:
    # Remove tools from Source Analyst.
    #
    # The Web Researcher already collected the sources.
    # This prevents CrewAI from sending the large
    # Web Page Reader tool definition to Groq.
    try:
        analyst.tools = []
    except Exception:
        pass

    source_analysis = run_single(
        analyst,
        f"""
Question:
{question}

Research collected by Web Researcher:
{research}

Analyze the supplied research.

For the most important sources identify:
- what evidence supports the answer
- source authority
- possible limitations
- possible inconsistencies

Do NOT search the web.

Use ONLY the supplied research.

Maximum 400 words.
""",
        "A short source analysis.",
        max_iterations=1,
    )

    source_analysis = trim_text(source_analysis, 1800)

    if on_agent_done:
        on_agent_done(2)

    # =====================================================
    # 4. FACT CHECKER
    # =====================================================

    if on_agent_start:
        on_agent_start(3, AGENT_NAMES[3])

    checker = create_fact_checker()

    # Remove any web-search tools from Fact Checker.
    try:
        checker.tools = []
    except Exception:
        pass

    fact_check = run_single(
        checker,
        f"""
Question:
{question}

Research:
{research}

Source analysis:
{source_analysis}

Check the supplied evidence.

Identify:
- supported claims
- questionable claims
- contradictions
- missing evidence
- limitations

Do NOT search the web.

Use ONLY the supplied material.

Maximum 300 words.
""",
        "A short fact-checking memo.",
        max_iterations=1,
    )

    fact_check = trim_text(fact_check, 1500)

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
Write the final report.

Question:
{question}

Research:
{research}

Source analysis:
{source_analysis}

Fact check:
{fact_check}

Use these sections:

1. Executive Summary
2. Key Findings
3. Detailed Analysis
4. Evidence & Sources
5. Uncertainty
6. Limitations
7. Conclusion
8. Sources

Use only the supplied information.

Do not invent URLs.

Keep the report concise.
""",
        "A concise final research report.",
        max_iterations=1,
    )

    report = trim_text(report, 6000)

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
