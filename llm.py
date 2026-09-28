
import os
from crewai import LLM

MODEL_NAME = "llama-3.3-70b-versatile"

def get_llm() -> LLM:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to Streamlit Secrets.")
    return LLM(
        model=f"groq/{MODEL_NAME}",
        api_key=api_key,
        temperature=0.2,
        max_completion_tokens=4096,
    )
