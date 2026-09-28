
from crewai import Agent
from llm import get_llm

def create_agent():
    return Agent(
        role="Research Manager",
        goal="Turn the user's research question into a precise, balanced research plan.",
        backstory=(
            "You are a senior research manager. You identify the important sub-questions, "
            "define what evidence is needed, and keep the investigation focused."
        ),
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
