
from crewai import Agent
from llm import get_llm
from tools import WebSearchTool

def create_agent():
    return Agent(
        role="Fact Checker",
        goal="Challenge the research findings and identify unsupported claims, conflicts and gaps.",
        backstory=(
            "You are a skeptical fact checker. You look for contradictions, outdated information, "
            "missing evidence and claims that should be qualified."
        ),
        tools=[WebSearchTool()],
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
