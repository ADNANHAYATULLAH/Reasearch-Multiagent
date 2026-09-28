
from crewai import Agent
from llm import get_llm

def create_agent():
    return Agent(
        role="Research Report Writer",
        goal="Create a clear, evidence-aware final report from the verified research material.",
        backstory=(
            "You are an expert research writer. You organize complex findings into a readable "
            "report, clearly separate evidence from interpretation, and preserve source URLs."
        ),
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
