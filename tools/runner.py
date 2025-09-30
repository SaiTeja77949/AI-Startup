"""
Code compilation and testing utilities for quality gates.
"""
import os
import sys
import tempfile
import subprocess
from typing import Tuple
from pathlib import Path

def py_compile_string(code: str) -> Tuple[bool, str]:
    """
    Compile Python code string using py_compile.
    
    Args:
        code: Python source code to compile
        
    Returns:
        Tuple of (success: bool, error_message: str)
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        try:
            # Write code to temporary file
            temp_file.write(code)
            temp_file.flush()
            
            # Run py_compile in a separate process
            result = subprocess.run(
                [sys.executable, '-m', 'py_compile', temp_file.name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return True, ""
            else:
                return False, result.stderr.strip()
                
        except Exception as e:
            return False, str(e)
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file.name)
            except:
                pass

def run_pytest_if_exists(work_dir: str) -> Tuple[bool, str]:
    """
    Run pytest if tests directory exists in the working directory.
    
    Args:
        work_dir: Directory to check for tests and run pytest in
        
    Returns:
        Tuple of (success: bool, output: str)
    """
    tests_dir = Path(work_dir) / 'tests'
    if not tests_dir.exists():
        return True, "No tests directory found"
        
    try:
        # Run pytest in quiet mode
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', '-q'],
            cwd=work_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            # Combine stdout and stderr for error details
            output = result.stdout.strip() + "\n" + result.stderr.strip()
            return False, output.strip()
            
    except Exception as e:
        return False, f"Error running pytest: {str(e)}"
