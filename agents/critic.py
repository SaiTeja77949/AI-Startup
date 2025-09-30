"""
Critic agent for code review and quality assurance.
"""
from crewai import Agent
from langchain_ollama import ChatOllama
from config import get_model_for_task, OLLAMA_HOST, OLLAMA_KEEP_ALIVE

def critic_agent() -> Agent:
    """Create a critic agent that outputs structured ReviewResult JSON."""
    llm = ChatOllama(
        model=f"ollama/{get_model_for_task('critic')}",
        base_url=OLLAMA_HOST,
        keep_alive=OLLAMA_KEEP_ALIVE,
        temperature=0.2
    )
    
    return Agent(
        role="Code Reviewer",
        goal=(
            "Review code and output a valid JSON ReviewResult object:\n"
            "- status: 'PASS' for clean code, 'ISSUES' if changes needed\n"
            "- diffs: [] for PASS, or list of suggested changes for ISSUES\n"
            "\nOutput ONLY the JSON object, no other text."
        ),
        backstory=(
            "You are a thorough code reviewer focused on correctness, imports, "
            "I/O handling, and edge cases. You provide specific, actionable feedback."
        ),
        llm=llm,
        verbose=True
    )