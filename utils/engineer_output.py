"""
Utilities for processing engineer output from the AI Startup Simulator.
Handles JSON extraction, content normalization, and file writing.
"""
import json
import re
from pathlib import Path
from typing import Any, Dict, Union

def extract_json_object(raw: str) -> dict:
    """
    Find the first JSON object in a raw string.
    
    Args:
        raw: Raw string that might contain a JSON object
        
    Returns:
        Extracted JSON object as a dictionary
        
    Raises:
        ValueError: If no valid JSON object is found
    """
    # Try to find JSON between code fences
    code_block_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
    match = re.search(code_block_pattern, raw)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Found code block but couldn't parse as JSON: {e}")
    
    # Try to find raw JSON object with curly braces
    object_pattern = r'(\{[\s\S]*\})'
    match = re.search(object_pattern, raw)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Found JSON-like content but couldn't parse: {e}")
    
    raise ValueError("No JSON object found in the engineer output")

def normalize_file_content(path: str, val: Any) -> str:
    """
    Normalize file content based on file path and value type.
    
    Args:
        path: File path including extension
        val: The value to normalize (could be str, dict, list, etc.)
        
    Returns:
        Normalized string content for the file
    """
    # If already a string, return as-is
    if isinstance(val, str):
        return val
    
    # Handle dictionaries and lists
    if isinstance(val, (dict, list)):
        if path.endswith(".json"):
            return json.dumps(val, indent=2)
        elif path.endswith(".js"):
            return f"module.exports = {json.dumps(val, indent=2)};\n"
        elif path.endswith(".ts"):
            return f"export default {json.dumps(val, indent=2)} as const;\n"
        else:
            return json.dumps(val, indent=2)
    
    # Fall back to string representation for any other type
    return str(val)

def write_files(base_dir: Path, files: Dict[str, Any]) -> int:
    """
    Write files to the filesystem with normalized content.
    
    Args:
        base_dir: Base directory to write files to
        files: Dictionary of file paths to content
        
    Returns:
        Number of files written
    """
    count = 0
    
    for file_path, content in files.items():
        full_path = base_dir / file_path
        
        # Create parent directories if they don't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Normalize the content and write to file
        normalized_content = normalize_file_content(file_path, content)
        full_path.write_text(normalized_content, encoding="utf-8")
        count += 1
    
    return count