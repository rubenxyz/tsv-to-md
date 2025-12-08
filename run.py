#!/usr/bin/env python3
"""
Wrapper script to activate virtual environment and run the TSV to TXT converter.

Usage:
    python3 run.py
"""
import os
import sys
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent

# Activate virtual environment and run main
if __name__ == "__main__":
    # Check if venv exists
    venv_path = PROJECT_ROOT / "venv"
    if not venv_path.exists():
        print("Error: Virtual environment not found. Run: python3 -m venv venv")
        sys.exit(1)
    
    # Path to Python in venv
    venv_python = venv_path / "bin" / "python3"
    
    # Execute the main module using venv Python
    os.execv(str(venv_python), [str(venv_python), "-m", "src.main"])
