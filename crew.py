
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

def run_single(agent, description, expected_output):
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
    return str(crew.kickoff())


def run_research(question, depth="Standard", on_agent_start=None, on_agent_done=None):
    if depth == "Quick":
        source_limit = "Use a compact set of the most useful sources."
    elif depth == "Deep":
        source_limit = "Use a broad set of sources and investigate important claims carefully."
    else:
        source_limit = "Use a balanced set of high-quality sources."

    # 1. Manager
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

        Create a practical research plan. Identify the major sub-questions,
        evidence requirements, source types to prioritize, and issues that need
        special verification. {source_limit}
        Do not write the final report.
        """,
        "A concise research plan with sub-questions, evidence requirements and source priorities.",
    )
    if on_agent_done:
        on_agent_done(0)

    # 2. Researcher
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

        Use your Live Web Search tool. Actually perform web searches.
        Prefer official organizations, original research, reputable technical
        documentation, universities, standards bodies and other authoritative
        sources where appropriate. Find current information and return source
        titles, URLs, dates when available, and concise evidence notes.
        {source_limit}
        Do not invent URLs or facts.
        """,
        "A source-backed research dossier containing useful findings and URLs.",
    )
    if on_agent_done:
        on_agent_done(1)

    # 3. Source analyst
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

        Use your Web Page Reader tool on the most important URLs from the dossier.
        Extract and assess evidence from the actual pages. Identify publication
        dates, relevant passages in your own words, source authority, context,
        limitations and any mismatch between the search snippet and the page.
        Focus on the sources most important to answering the question.
        """,
        "A source-analysis dossier containing verified evidence, source quality notes and URLs.",
    )
    if on_agent_done:
        on_agent_done(2)

    # 4. Fact checker
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

        Use your Live Web Search tool to independently verify important,
        uncertain or potentially outdated claims. Identify:
        - supported claims
        - unsupported claims
        - conflicting claims
        - information that requires qualification
        - important gaps

        Do not invent evidence. Explain what should and should not appear
        as a firm statement in the final report.
        """,
        "A fact-checking memo with supported claims, conflicts, gaps and recommended qualifications.",
    )
    if on_agent_done:
        on_agent_done(3)

    # 5. Writer
    if on_agent_start:
        on_agent_start(4, AGENT_NAMES[4])

    writer = create_report_writer()
    report = run_single(
        writer,
        f"""
        Write the final research report for this question:

        {question}

        Research plan:
        {plan}

        Web research:
        {research}

        Source analysis:
        {source_analysis}

        Fact-checking memo:
        {fact_check}

        Create a polished report with:
        1. Executive Summary
        2. Key Findings
        3. Detailed Analysis
        4. Evidence & Source Notes
        5. Conflicting or Uncertain Information
        6. Limitations
        7. Conclusion
        8. Sources

        Keep facts traceable to the supplied URLs. Do not create citations
        or URLs that were not present in the research material. Clearly label
        uncertainty and avoid presenting speculation as fact.
        """,
        "A polished, evidence-aware research report with a source list.",
    )
    if on_agent_done:
        on_agent_done(4)

    return {
        "report": report,
        "sources": extract_sources(research),
    }


def extract_sources(text):
    sources = []
    seen = set()
    for line in text.splitlines():
        if line.strip().lower().startswith("url:"):
            url = line.split(":", 1)[1].strip()
            if url.startswith(("http://", "https://")) and url not in seen:
                seen.add(url)
                sources.append({"title": "Research source", "url": url})
    return sources[:12]
