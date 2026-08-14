"""
Voice & CLI Virtual Assistant Main Entry Point.
"""

import os
import sys

# Ensure src is in Python module search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.cli import run_cli

if __name__ == "__main__":
    run_cli()
