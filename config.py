"""
Configuration management for AI Startup Simulator.
Handles environment variables and model routing logic.
"""
import os
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ollama Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_KEEP_ALIVE = os.getenv("OLLAMA_KEEP_ALIVE", "10m")

# Default Models
DEFAULT_RESEARCH_MODEL = "llama3.1:8b-instruct-q4_K_M"
DEFAULT_CODER_MODEL = "qwen2.5-coder:7b-instruct-q5_1"

# Model Configuration
MODEL_RESEARCH = os.getenv("MODEL_RESEARCH", DEFAULT_RESEARCH_MODEL)
MODEL_CODER = os.getenv("MODEL_CODER", DEFAULT_CODER_MODEL)
HEAVY_REASONER = os.getenv("HEAVY_REASONER", "")
USE_HEAVY_FOR = os.getenv("USE_HEAVY_FOR", "").lower().split(",")

# Redis Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# GitHub Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# File System Paths
ARTIFACTS_DIR = os.path.join("artifacts")
LOGS_DIR = os.path.join("logs")
STATE_DIR = os.path.join("state")
DB_PATH = os.path.join(STATE_DIR, "app.db")

def get_model_for_task(task: str) -> str:
    """
    Route tasks to appropriate models based on configuration.
    
    Args:
        task: Task identifier ('research', 'engineer', 'critic', 'marketing')
        
    Returns:
        Model identifier to use for the task
    """
    if HEAVY_REASONER and task in USE_HEAVY_FOR:
        return HEAVY_REASONER
        
    if task in ['engineer', 'critic']:
        return MODEL_CODER
    
    return MODEL_RESEARCH  # Default for research and marketing

def ensure_directories():
    """Create necessary directories if they don't exist."""
    for directory in [ARTIFACTS_DIR, LOGS_DIR, STATE_DIR]:
        os.makedirs(directory, exist_ok=True)

# Create directories on module import
ensure_directories()
