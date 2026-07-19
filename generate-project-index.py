#!/usr/bin/env python3
import os
import json
import re
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
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

COMMON_LIBS = {
    "numpy": "numpy",
    "pandas": "pandas",
    "sklearn": "scikit-learn",
    "scikit-learn": "scikit-learn",
    "tensorflow": "tensorflow",
    "keras": "keras",
    "torch": "pytorch",
    "pytorch": "pytorch",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "nltk": "nltk",
    "cv2": "opencv",
    "opencv": "opencv",
    "xgboost": "xgboost",
    "lightgbm": "lightgbm",
    "spacy": "spacy",
    "transformers": "transformers",
    "bs4": "beautifulsoup4",
    "requests": "requests",
    "statsmodels": "statsmodels",
    "prophet": "prophet",
    "yolo": "yolo",
}

def clean_name(folder_name):
    # Replace underscores/hyphens with spaces and capitalize
    name = folder_name.replace("_", " ").replace("-", " ")
    # Strip double spaces
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def parse_notebook(notebook_path):
    metadata = {
        "name": None,
        "description": None,
        "technologies": set(),
        "category": set()
    }
    try:
        with open(notebook_path, "r", encoding="utf-8", errors="ignore") as f:
            data = json.load(f)
            cells = data.get("cells", [])
            
            # Extract name and description from first few markdown cells
            markdown_text = ""
            for cell in cells:
                if cell.get("cell_type") == "markdown":
                    source = "".join(cell.get("source", []))
                    if not metadata["name"]:
                        # Look for # Header
                        match = re.search(r"^#\s+(.+)$", source, re.MULTILINE)
                        if match:
                            metadata["name"] = match.group(1).strip()
                    markdown_text += " " + source

                elif cell.get("cell_type") == "code":
                    source = "".join(cell.get("source", []))
                    # Scan for imports
                    for line in source.split("\n"):
                        # Match: import module, import module as alias, from module import ...
                        import_match = re.match(r"^\s*(?:import|from)\s+([a-zA-Z0-9_]+)", line)
                        if import_match:
                            lib = import_match.group(1).lower()
                            if lib in COMMON_LIBS:
                                metadata["technologies"].add(COMMON_LIBS[lib])

            # Guess category from markdown and name
            full_text = (notebook_path.name + " " + markdown_text).lower()
            if "classification" in full_text:
                metadata["category"].add("classification")
            if "regression" in full_text:
                metadata["category"].add("regression")
            if "nlp" in full_text or "text" in full_text or "sentiment" in full_text or "chatbot" in full_text:
                metadata["category"].add("nlp")
            if "vision" in full_text or "image" in full_text or "detection" in full_text or "cnn" in full_text:
                metadata["category"].add("computer-vision")
            if "forecast" in full_text or "time series" in full_text:
                metadata["category"].add("time-series")
            if "cluster" in full_text:
                metadata["category"].add("clustering")
            if "reinforcement" in full_text or "q-learning" in full_text:
                metadata["category"].add("reinforcement-learning")

            # Extract first line/sentence as description if possible
            sentences = re.split(r'[.!?]\s+', markdown_text.strip())
            for s in sentences:
                s_clean = re.sub(r'[#*`_\-\n]+', ' ', s).strip()
                s_clean = re.sub(r'\s+', ' ', s_clean)
                if len(s_clean) > 20 and not s_clean.startswith("http"):
                    metadata["description"] = s_clean[:150]
                    if len(s_clean) > 150:
                        metadata["description"] += "..."
                    break
    except Exception as e:
        print(f"Warning: Failed to parse notebook {notebook_path}: {e}")
    
    return metadata

def scan_projects():
    existing_projects = {}
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for proj in data:
                    if "path" in proj:
                        existing_projects[proj["path"]] = proj
        except Exception as e:
            print(f"Warning: Could not read existing index file: {e}")

    projects = []
    
    for entry in os.listdir(ROOT_DIR):
        dir_path = ROOT_DIR / entry
        if not dir_path.is_dir():
            continue
        if entry in EXCLUDED_DIRS or entry.startswith("."):
            continue

        # Look for notebook or python script
        notebooks = list(dir_path.glob("*.ipynb"))
        py_scripts = list(dir_path.glob("*.py"))
        
        if not notebooks and not py_scripts:
            # Check one level deeper for nested notebooks (optional, but keep it clean)
            notebooks = list(dir_path.glob("**/*.ipynb"))
            py_scripts = list(dir_path.glob("**/*.py"))
            
        if not notebooks and not py_scripts:
            continue # Not a project folder

        # Determine relative path of the main notebook/script
        main_notebook = None
        if notebooks:
            # Try to match name or pick first
            main_notebook = sorted(notebooks, key=lambda p: len(p.name))[0]
        
        has_requirements = (dir_path / "requirements.txt").exists()
        has_readme = (dir_path / "README.md").exists()
        
        # Load or generate metadata
        proj_path = entry
        existing = existing_projects.get(proj_path, {})
        
        notebook_rel = str(main_notebook.relative_to(dir_path)).replace("\\", "/") if main_notebook else None
        
        # Parse details from notebook
        extracted = {}
        if main_notebook:
            extracted = parse_notebook(main_notebook)
            
        name = existing.get("name") or extracted.get("name") or clean_name(entry)
        description = existing.get("description") or extracted.get("description") or f"Machine learning project for {clean_name(entry)}"
        difficulty = existing.get("difficulty") or "beginner"
        
        # Merge technologies and categories
        tech_set = set(existing.get("technologies", []))
        if extracted.get("technologies"):
            tech_set.update(extracted["technologies"])
        technologies = sorted(list(tech_set)) if tech_set else ["python"]
        
        cat_set = set(existing.get("category", []))
        if extracted.get("category"):
            cat_set.update(extracted["category"])
        # If no category detected, try to infer from common directory naming
        if not cat_set:
            path_lower = entry.lower()
            if "classification" in path_lower:
                cat_set.add("classification")
            elif "regression" in path_lower:
                cat_set.add("regression")
            elif "nlp" in path_lower or "chatbot" in path_lower:
                cat_set.add("nlp")
            elif "detection" in path_lower or "image" in path_lower or "vision" in path_lower or "yolo" in path_lower:
                cat_set.add("computer-vision")
            elif "forecast" in path_lower or "time" in path_lower:
                cat_set.add("time-series")
            else:
                cat_set.add("machine-learning")
        category = sorted(list(cat_set))
        
        author = existing.get("author") or "contributor"
        
        projects.append({
            "name": name,
            "path": proj_path,
            "description": description,
            "difficulty": difficulty,
            "category": category,
            "technologies": technologies,
            "author": author,
            "has_requirements": has_requirements,
            "has_readme": has_readme,
            "notebook": notebook_rel
        })

    # Sort projects alphabetically by path
    projects.sort(key=lambda p: p["path"].lower())
    
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)
        f.write("\n")
        
    print(f"Successfully generated/updated project-index.json with {len(projects)} projects.")

if __name__ == "__main__":
    scan_projects()
