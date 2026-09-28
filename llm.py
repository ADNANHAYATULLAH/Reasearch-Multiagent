import os

# Workaround for a current CrewAI/Groq cache-breakpoint
# compatibility issue.
try:
    import crewai.llms.cache as crew_cache

    crew_cache.mark_cache_breakpoint = lambda msg: msg

except Exception:
    pass

from crewai import LLM


# Current Groq production model
MODEL_NAME = "openai/gpt-oss-120b"


def get_llm() -> LLM:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. "
            "Add it in Streamlit Secrets."
        )

    return LLM(
        model=f"groq/{MODEL_NAME}",
        api_key=api_key,
        temperature=0.2,
        max_completion_tokens=2000,
    )
