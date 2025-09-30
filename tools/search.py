"""Tiny wrapper around DuckDuckGo text search.

This module prefers the modern `ddgs` package but falls back to the
older `duckduckgo_search` package for compatibility. Install one of
them in your environment (recommended: `ddgs`).
"""
from typing import List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

try:
    # preferred package (new name)
    from ddgs import DDGS  # type: ignore
except Exception:
    try:
        # backward-compatible name used in some environments
        from duckduckgo_search import DDGS  # type: ignore
    except Exception as exc:  # pragma: no cover - environment issue
        raise ImportError(
            "Missing search backend: install the 'ddgs' package (recommended) or 'duckduckgo-search'."
        ) from exc


class WebSearchToolSchema(BaseModel):
    """Schema for the web_search tool."""
    query: str = Field(description="The search query string")
    max_results: int = Field(5, description="Maximum number of results to return")


class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search the web for information. Returns a list of relevant results with titles and URLs."
    args_schema: type[BaseModel] = WebSearchToolSchema

    def __init__(self):
        super().__init__()

    def _run(self, query: str, max_results: int = 5) -> str:
        """Lightweight web search. Returns title + URL bullets as text.

        Inputs:
          - query: search query string
          - max_results: max number of results to return

        Output: newline-delimited bullet list (or 'No results.').
        """
        results: List[str] = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                # result shape varies slightly across versions; guard safely
                title = (r.get("title") or "").strip()
                href = (r.get("href") or r.get("url") or "").strip()
                if title and href:
                    results.append(f"- {title} — {href}")
        return "\n".join(results) if results else "No results."

# Create tool instance
web_search = WebSearchTool()