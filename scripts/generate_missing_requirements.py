#!/usr/bin/env python3

"""Generate requirements.txt files for project folders missing them.

The script scans top-level project directories, inspects Python notebooks and
scripts for imports, and writes a flat requirements.txt file with the inferred
third-party packages. It intentionally keeps the output lightweight so it fits
the repository's existing requirements files.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from json import JSONDecodeError


ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRECTORIES = {
    ".git",
    "__pycache__",
    "docs",
    "scripts",
    "site",
    "website",
    "Sql",
}

MODULE_TO_PACKAGE = {
    "bs4": "beautifulsoup4",
    "cv2": "opencv-python",
    "github": "PyGithub",
    "face_recognition": "face-recognition",
    "fbprophet": "prophet",
    "imblearn": "imbalanced-learn",
    "keras": "keras",
    "lightgbm": "lightgbm",
    "markdown2": "markdown2",
    "matplotlib": "matplotlib",
    "mpl_toolkits": "matplotlib",
    "nltk": "nltk",
    "opencv": "opencv-python",
    "PIL": "pillow",
    "pandas": "pandas",
    "plotly": "plotly",
    "prophet": "prophet",
    "pyttsx3": "pyttsx3",
    "pyzbar": "pyzbar",
    "requests": "requests",
    "scipy": "scipy",
    "seaborn": "seaborn",
    "sklearn": "scikit-learn",
    "spacy": "spacy",
    "statsmodels": "statsmodels",
    "streamlit": "streamlit",
    "tensorflow": "tensorflow",
    "torch": "torch",
    "torchvision": "torchvision",
    "torchaudio": "torchaudio",
    "transformers": "transformers",
    "xgboost": "xgboost",
    "yaml": "pyyaml",
    "yfinance": "yfinance",
}

STD_LIBS = set(getattr(sys, "stdlib_module_names", set()))


def is_third_party(module_name: str) -> bool:
    root = module_name.split(".", 1)[0]
    return root not in STD_LIBS and root not in {"__future__", "typing"}


def normalize_package(module_name: str) -> str:
    root = module_name.split(".", 1)[0]
    return MODULE_TO_PACKAGE.get(root, root)


def strip_magics(source: str) -> str:
    cleaned_lines = []
    for line in source.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("%", "!", "?")):
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


def imports_from_source(source: str) -> set[str]:
    modules: set[str] = set()
    try:
        tree = ast.parse(strip_magics(source))
    except SyntaxError:
        return modules

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def imports_from_file(path: Path) -> set[str]:
    if path.suffix == ".py":
        return imports_from_source(path.read_text(encoding="utf-8"))

    if path.suffix == ".ipynb":
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, JSONDecodeError):
            return set()
        modules: set[str] = set()
        for cell in notebook.get("cells", []):
            if cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", []))
            modules.update(imports_from_source(source))
        return modules

    return set()


def project_directories() -> list[Path]:
    directories = []
    for path in sorted(ROOT.iterdir(), key=lambda item: item.name.lower()):
        if not path.is_dir() or path.name.startswith("."):
            continue
        if path.name in SKIP_DIRECTORIES:
            continue
        directories.append(path)
    return directories


def code_files(project_dir: Path) -> list[Path]:
    files = []
    for path in project_dir.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.suffix in {".py", ".ipynb"} and path.is_file():
            files.append(path)
    return files


def infer_requirements(project_dir: Path) -> list[str]:
    modules: set[str] = set()
    for path in code_files(project_dir):
        modules.update(imports_from_file(path))

    packages = {
        normalize_package(module)
        for module in modules
        if is_third_party(module)
    }
    return sorted(packages, key=str.lower)


def main() -> int:
    created = []
    skipped = []

    for project_dir in project_directories():
        requirements = project_dir / "requirements.txt"
        if requirements.exists():
            skipped.append(project_dir.name)
            continue

        code_paths = code_files(project_dir)
        if not code_paths:
            continue

        packages = infer_requirements(project_dir)
        content = (
            "# Auto-generated from notebook and Python imports\n"
            if not packages
            else "\n".join(packages) + "\n"
        )
        requirements.write_text(content, encoding="utf-8")
        created.append((project_dir.name, len(packages)))

    print(f"Created {len(created)} requirements.txt files")
    for name, count in created[:20]:
        print(f"- {name}: {count} packages")
    if len(created) > 20:
        print(f"- ... {len(created) - 20} more")
    print(f"Skipped {len(skipped)} existing requirements.txt files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())