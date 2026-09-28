
from crewai import Agent
from llm import get_llm
from tools import WebSearchTool

def create_agent():
    return Agent(
        role="Web Researcher",
        goal="Find current, relevant and diverse web sources that answer the research question.",
        backstory=(
            "You are an investigative web researcher. You search deliberately, prefer primary "
            "and authoritative sources, and record URLs and useful evidence."
        ),
        tools=[WebSearchTool()],
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
