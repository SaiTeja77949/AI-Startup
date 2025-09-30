import argparse, pathlib
from crewai import Crew, Task, Process
from agents.research import research_agent
from agents.engineer import engineer_agent
from agents.critic import critic_agent
from agents.marketing import marketing_agent
from utils.engineer_output import extract_json_object, write_files

ART = pathlib.Path("artifacts"); ART.mkdir(exist_ok=True)

def save(name: str, text: str):
    (ART / name).write_text(text, encoding="utf-8")

def build_crew(idea: str):
    r = research_agent(); e = engineer_agent(); c = critic_agent(); m = marketing_agent()

    t1 = Task(
        description=(f"Research the idea: {idea}\n"
                     "- List 3–5 user pain points\n- 3 competing solutions with URLs\n"
                     "- A short actionable spec with 3–5 requirements\n\n"
                     "Use web_search(query) where helpful.\nOutput in markdown."),
        agent=r,
        expected_output="Markdown with bullets + links + a short spec"
    )

    t2 = Task(
        description=(
            "Generate a complete Next.js app (TypeScript) as a single JSON object.\n"
            "Keys = file paths, Values = entire file content as a string.\n"
            f"This should be a fully functional Next.js application based on this idea: {idea}\n\n"
            "Use the research from the previous task to guide your implementation.\n\n"
            "Rules:\n"
            "1. Do not return nested objects for files. All values must be strings.\n"
            "2. For JSON files (e.g., package.json), return a serialized JSON string (minified or pretty).\n"
            "3. For .js/.ts config files, return valid code (ESM) as a string (no JS objects).\n"
            "4. Include ALL necessary files for a functional Next.js app (pages, components, styles, API services, etc.)\n"
            "5. No Markdown fences or prose. Output ONLY the JSON object.\n"
            "6. Include TypeScript types and interfaces for all components and data structures.\n"
            "7. Ensure proper error handling and loading states throughout the application.\n"
        ),
        agent=e,
        expected_output="A JSON object representing the complete file structure of a Next.js application based on the idea."
    )

    t3 = Task(
        description=("Review the following code. If issues: start with 'ISSUES FOUND', "
                     "list fixes and diffs. If clean: 'PASS'.\n\n<CODE>{{output_of_previous_task}}</CODE>"),
        agent=c,
        expected_output="PASS or issues with diffs"
    )

    t4 = Task(
        description=("Write a launch post (150–250 words) using the spec and final feature list."),
        agent=m,
        expected_output="Launch copy"
    )

    crew = Crew(
        agents=[r, e, c, m],
        tasks=[t1, t2, t3, t4],
        process=Process.sequential,
        memory=False,      # we keep MVP simple; can enable later
        verbose=True
    )
    return crew

import json5 as json
import re

def extract_json_from_string(s: str) -> str:
    """Extracts the first JSON object from a string. DEPRECATED: Use utils.engineer_output.extract_json_object instead."""
    # Try to find JSON between triple backticks
    code_block_pattern = r'```(?:json)?\s*(\{.*?\})```'
    match = re.search(code_block_pattern, s, re.DOTALL)
    if match:
        return match.group(1)
    
    # Fall back to just looking for curly braces
    match = re.search(r'\{.*\}', s, re.DOTALL)
    if match:
        return match.group(0)
    
    # If nothing found, return empty JSON
    return "{}"

def run(idea: str):
    crew = build_crew(idea)
    result = crew.kickoff()

    # Grab per-task outputs from the CrewOutput returned by kickoff(); fall back to string if raw missing
    outs = result.tasks_output
    save("research.md", outs[0].raw or str(outs[0]))

    # The engineer agent now outputs a JSON string. We need to parse it.
    raw_output = outs[1].raw or "{}"
    
    # Save the raw engineer output to a file
    save("engineer_raw.json", raw_output)
    print("\nSaved raw engineer output to artifacts/engineer_raw.json")
    
    print("Parsing engineer output...")
    
    try:
        # Extract the JSON object from the raw output
        file_structure = extract_json_object(raw_output)
        
        # Create the directory for the Next.js app
        app_dir = ART / "nextjs_app"
        app_dir.mkdir(exist_ok=True)
        
        # Write the files using our utility function
        file_count = write_files(app_dir, file_structure)
        print(f"Created {file_count} files in {app_dir}")
        
    except Exception as e:
        print(f"Error processing engineer output: {e}")
        save("error_log.txt", f"Error: {e}\n\nRaw Output:\n{raw_output}")
        print("Error saved to artifacts/error_log.txt")
        # Continue with the rest of the process

    save("review.md", outs[2].raw or str(outs[2]))
    save("launch.md", outs[3].raw or str(outs[3]))

    print("\n✅ Done. See artifacts/: research.md, engineer_raw.json, nextjs_app/, review.md, launch.md")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("idea", help="Product idea to simulate")
    args = ap.parse_args()
    run(args.idea)