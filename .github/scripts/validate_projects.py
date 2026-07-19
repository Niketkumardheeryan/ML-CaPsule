#!/usr/bin/env python3
import os
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
INDEX_FILE = ROOT_DIR / "project-index.json"

EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".idea",
    "tests",
    "img",
    "__pycache__",
    "Dataset_Resources",
    "Cheat Sheets",
    "Basics of ML and DL",
    "Basics of Power Bi",
    "Basics of the Python",
    "File of SQL Commands",
    "MLOps-for-Beginners",
    "MLOps_Learning_Module",
    "Prompt_Engineering_Techniques",
    "R language",
    "Sql",
    "Various Plots using Matplot,Seaborn,Pandas",
    "website ML-CaPsule",
    "website",
}

def get_disk_projects():
    projects = set()
    for entry in os.listdir(ROOT_DIR):
        dir_path = ROOT_DIR / entry
        if not dir_path.is_dir():
            continue
        if entry in EXCLUDED_DIRS or entry.startswith("."):
            continue
            
        notebooks = list(dir_path.glob("*.ipynb"))
        py_scripts = list(dir_path.glob("*.py"))
        
        if not notebooks and not py_scripts:
            # Check one level deeper for nested notebooks/scripts
            notebooks = list(dir_path.glob("**/*.ipynb"))
            py_scripts = list(dir_path.glob("**/*.py"))
            
        if notebooks or py_scripts:
            projects.add(entry)
            
    return projects

def validate():
    print("Starting project index validation...")
    
    if not INDEX_FILE.exists():
        print(f"ERROR: {INDEX_FILE} does not exist.")
        sys.exit(1)
        
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: project-index.json is not valid JSON: {e}")
        sys.exit(1)
        
    if not isinstance(data, list):
        print("ERROR: project-index.json root element must be a JSON array.")
        sys.exit(1)
        
    errors = 0
    indexed_paths = []
    
    for idx, proj in enumerate(data):
        if not isinstance(proj, dict):
            print(f"ERROR: Entry at index {idx} is not a JSON object.")
            errors += 1
            continue
            
        path = proj.get("path")
        if not path:
            print(f"ERROR: Entry at index {idx} is missing the 'path' key.")
            errors += 1
            continue
            
        indexed_paths.append(path)
        
        # Verify required keys exist
        required_keys = ["name", "path", "description", "difficulty", "category", "technologies", "author", "has_requirements", "has_readme", "notebook"]
        for key in required_keys:
            if key not in proj:
                print(f"ERROR: Project '{path}' is missing the required metadata key '{key}'.")
                errors += 1
                
    # Check sorting
    sorted_paths = sorted(indexed_paths, key=lambda p: p.lower())
    if indexed_paths != sorted_paths:
        print("ERROR: project-index.json is not sorted alphabetically by path (case-insensitive).")
        # Find first misordered item
        for a, b in zip(indexed_paths, sorted_paths):
            if a != b:
                print(f"  First mismatch: expected '{b}' but found '{a}'.")
                break
        errors += 1
        
    # Check filesystem alignment
    disk_projects = get_disk_projects()
    indexed_set = set(indexed_paths)
    
    # 1. Check if all indexed projects exist on disk
    for path in indexed_paths:
        if path not in disk_projects:
            print(f"ERROR: Project path '{path}' listed in index does not exist or has no notebooks/scripts on disk.")
            errors += 1
            
    # 2. Check if all projects on disk are in the index
    for path in disk_projects:
        if path not in indexed_set:
            print(f"ERROR: Project directory '{path}' exists on disk but is not registered in project-index.json.")
            print("  Please run: python generate-project-index.py to update the index.")
            errors += 1

    if errors > 0:
        print(f"Validation FAILED with {errors} errors.")
        sys.exit(1)
        
    print(f"Validation PASSED. {len(data)} projects successfully verified.")

if __name__ == "__main__":
    validate()
