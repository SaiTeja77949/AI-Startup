"""
Test script to verify agent functionality.
"""
import json
from crewai import Crew, Task
from agents.research import research_agent
from agents.engineer import engineer_agent
from agents.critic import critic_agent
from agents.marketing import marketing_agent

def test_agents():
    # Create the agents
    researcher = research_agent()
    engineer = engineer_agent()
    critic = critic_agent()
    marketer = marketing_agent()
    
    # Create tasks
    research_task = Task(
        description="Research and provide a ResearchSpec JSON for: 'A CLI tool that helps developers manage their git branches and automates cleanup of stale branches.'",
        agent=researcher,
        expected_output="A valid JSON ResearchSpec object with pain points, competitors, and requirements."
    )
    
    engineer_task = Task(
        description="Using the research results, implement a single Python file that solves this problem. Output only the code.",
        agent=engineer,
        expected_output="A complete, runnable Python implementation."
    )
    
    critic_task = Task(
        description="Review the implementation and provide a ReviewResult JSON with your findings.",
        agent=critic,
        expected_output="A valid JSON ReviewResult object with status and optional diffs."
    )
    
    marketing_task = Task(
        description="Using the research and implementation, write launch copy for the product.",
        agent=marketer,
        expected_output="A 150-250 word launch post with problem, solution, features, and CTA."
    )
    
    # Create a crew
    crew = Crew(
        agents=[researcher, engineer, critic, marketer],
        tasks=[research_task, engineer_task, critic_task, marketing_task],
        verbose=True
    )
    
    # Run the crew
    results = crew.kickoff()
    
    # Print results with clear separation
    for i, result in enumerate(results):
        print(f"\n{'='*80}\nTask {i+1} Result:\n{'='*80}")
        print(result)
        print()

if __name__ == "__main__":
    test_agents()