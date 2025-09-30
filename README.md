# AI Startup Simulator

This project is a multi-agent AI system that takes a product idea and generates a complete software project, including source code, documentation, and marketing materials.

## Current State (MVP)

The current implementation is a command-line tool that runs a sequential pipeline of AI agents to generate project artifacts.

- **`main.py`**: The entry point for the CLI application.
- **`agents/`**: Contains the definitions for the different AI agents (Research, Engineer, Critic, Marketing).
- **`tools/`**: Contains helper tools, like the web search utility.
- **`artifacts/`**: The output directory where all generated files are saved.
- **`requirements.txt`**: Lists the Python dependencies.

## How to Run

1.  **Set up the environment:**
    - Create a virtual environment: `python -m venv venv`
    - Activate it: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
    - Install dependencies: `pip install -r requirements.txt`

2.  **Run the simulator:**
    - Execute the main script with your product idea:
      ```sh
      python main.py "A web app that helps people find local pickup basketball games"
      ```

3.  **Check the output:**
    - The generated files will be in the `artifacts/` directory.

## Next Steps (Service Layer)

The next major milestone is to wrap this functionality in a web service.

- **API Server (FastAPI)**:
    - `POST /run`: Submit a new product idea.
    - `GET /jobs/:id`: Check the status of a job.
- **Background Worker (Celery/RQ)**:
    - Process jobs asynchronously.
- **Database (SQLite/Postgres)**:
    - Store job state and metadata.

This will evolve the project from a simple CLI tool to a scalable, asynchronous service.
