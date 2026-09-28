
from crewai import Agent
from llm import get_llm
from tools import WebFetchTool

def create_agent():
    return Agent(
        role="Source Analyst",
        goal="Inspect important source pages and extract evidence that can safely support the report.",
        backstory=(
            "You are a source-evaluation specialist. You distinguish claims from evidence, "
            "note dates and context, and flag weak or incomplete sources."
        ),
        tools=[WebFetchTool()],
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
