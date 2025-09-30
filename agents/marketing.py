"""
Marketing agent for launch copy generation.
"""
from crewai import Agent
from langchain_ollama import ChatOllama
from config import get_model_for_task, OLLAMA_HOST, OLLAMA_KEEP_ALIVE

def marketing_agent() -> Agent:
    """Create a marketing agent that writes launch copy."""
    llm = ChatOllama(
        model=f"ollama/{get_model_for_task('marketing')}",
        base_url=OLLAMA_HOST,
        keep_alive=OLLAMA_KEEP_ALIVE,
        temperature=0.5
    )
    
    return Agent(
        role="Product Marketing",
        goal=(
            "Write a compelling 150-250 word launch post following this structure:\n"
            "1. Problem statement\n"
            "2. Solution overview\n"
            "3. Key features (3-5)\n"
            "4. Call to action\n"
            "\nOutput ONLY the formatted text, no additional markup."
        ),
        backstory=(
            "You are a skilled product marketer who creates clear, engaging copy "
            "that resonates with developers and technical audiences."
        ),
        llm=llm,
        verbose=True
    )