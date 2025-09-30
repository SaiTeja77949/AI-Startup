"""
Research agent for market analysis and requirements gathering.
"""
from crewai import Agent
from langchain_ollama import ChatOllama
from tools.search import web_search
from config import get_model_for_task, OLLAMA_HOST, OLLAMA_KEEP_ALIVE

def research_agent() -> Agent:
    """Create a research agent that outputs structured ResearchSpec JSON."""
    llm = ChatOllama(
        model=f"ollama/{get_model_for_task('research')}",
        base_url=OLLAMA_HOST,
        keep_alive=OLLAMA_KEEP_ALIVE,
        temperature=0.3
    )
    
    return Agent(
        role="Market Research & Spec",
        goal=(
            "Research the market and output a valid JSON ResearchSpec object with:\n"
            "- pain_points: 3-5 key problems solved\n"
            "- competitors: exactly 3 items as 'Name - URL'\n"
            "- requirements: 3-5 actionable implementation points\n"
            "\nOutput ONLY the JSON object, no other text."
        ),
        backstory=(
            "You are a pragmatic product researcher who delivers structured insights "
            "in a clear JSON format. You validate competitors through web search."
        ),
        llm=llm,
        tools=[web_search],
        allow_delegation=False,
        verbose=True
    )