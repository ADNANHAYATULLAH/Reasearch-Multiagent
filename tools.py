
from typing import Type
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from ddgs import DDGS


class WebSearchInput(BaseModel):
    query: str = Field(..., description="A focused web search query.")
    max_results: int = Field(6, ge=1, le=10, description="Maximum number of search results.")


class WebSearchTool(BaseTool):
    name: str = "Live Web Search"
    description: str = (
        "Search the live web for current information. Use this when you need "
        "recent facts, sources, dates, organizations, research, or technical information."
    )
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str, max_results: int = 6) -> str:
        try:
            results = DDGS().text(query, max_results=max_results)
            if not results:
                return "No search results were returned."
            lines = []
            for i, item in enumerate(results, 1):
                title = item.get("title", "Untitled")
                url = item.get("href") or item.get("url") or ""
                snippet = item.get("body") or item.get("snippet") or ""
                lines.append(f"{i}. {title}\nURL: {url}\nSnippet: {snippet}")
            return "\n\n".join(lines)
        except Exception as exc:
            return f"Web search failed: {exc}"


class WebFetchInput(BaseModel):
    url: str = Field(..., description="A full http or https URL to retrieve.")


class WebFetchTool(BaseTool):
    name: str = "Web Page Reader"
    description: str = (
        "Fetch and extract readable text from a public web page. Use this to inspect "
        "a source URL rather than relying only on a search snippet."
    )
    args_schema: Type[BaseModel] = WebFetchInput

    def _run(self, url: str) -> str:
        if not url.startswith(("http://", "https://")):
            return "Invalid URL. Use a full http:// or https:// URL."
        try:
            response = requests.get(
                url,
                timeout=15,
                headers={"User-Agent": "ResearchForgeAI/1.0"},
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(["script", "style", "noscript", "svg"]):
                tag.decompose()
            text = soup.get_text(" ", strip=True)
            if len(text) > 12000:
                text = text[:12000] + "\n[Page text truncated]"
            return text or "No readable text was found on this page."
        except Exception as exc:
            return f"Page retrieval failed: {exc}"
