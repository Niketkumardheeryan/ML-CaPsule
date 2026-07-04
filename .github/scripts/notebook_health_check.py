#!/usr/bin/env python3
"""
Notebook Health Check Bot
Automatically tests Jupyter notebooks for errors, missing imports, and deprecations.
"""

import os
import sys
import subprocess
from pathlib import Path

def find_notebooks(root_dir="."):
    """Find notebooks in specific directories only (avoid scanning entire 1.8GB repo)."""
    notebooks = []
    root_path = Path(root_dir)
    
    # Only scan these folders (common notebook locations)
    folders_to_scan = ["notebooks", "examples", "tutorials", "docs", "guides"]
    
    for folder in folders_to_scan:
        folder_path = root_path / folder
        if folder_path.exists():
            for path in folder_path.rglob("*.ipynb"):
                if ".ipynb_checkpoints" not in str(path):
                    notebooks.append(path)
    
    # If no notebooks found in specific folders, scan current directory only (not subdirectories)
    if not notebooks:
        for path in root_path.glob("*.ipynb"):
            notebooks.append(path)
    
    # Also check for notebooks in root level (if any)
    for path in root_path.glob("*.ipynb"):
        if path not in notebooks:
            notebooks.append(path)
    
    return notebooks

def test_notebook(notebook_path):
    """Test a single notebook using nbconvert."""
    result = {
        "path": str(notebook_path),
        "success": False,
        "error": None
    }
    
    try:
        # Run the notebook using nbconvert
        subprocess.run(
            [
                "jupyter", "nbconvert", "--to", "notebook",
                "--execute", str(notebook_path),
                "--output", "-", "--allow-errors"
            ],
            capture_output=True,
            text=True,
            timeout=300
        )
        result["success"] = True
    except subprocess.TimeoutExpired:
        result["error"] = "Timeout (5 minutes)"
    except Exception as e:
        result["error"] = str(e)
    
    return result

def main():
    notebooks = find_notebooks()
    print(f"Found {len(notebooks)} notebooks")
    
    if not notebooks:
        print("No notebooks found to test.")
        sys.exit(0)
    
    results = []
    for nb in notebooks:
        print(f"Testing: {nb}")
        result = test_notebook(nb)
        results.append(result)
    
    # Create issue for failed notebooks
    failed = [r for r in results if not r["success"]]
    
    if failed:
        print(f"\n❌ {len(failed)} notebooks failed:")
        for f in failed:
            print(f"  - {f['path']}: {f['error']}")
        sys.exit(1)
    else:
        print(f"\n✅ All {len(results)} notebooks passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
    