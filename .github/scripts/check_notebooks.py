#!/usr/bin/env python3
"""Static quality checks for Jupyter notebooks.

This complements `notebook_health_check.py` rather than repeating it: that
script *executes* notebooks to see whether they still run, while this one reads
the file and looks for problems that are visible without running anything.

Checks performed
----------------
errors (fail the job)
    * the file is not valid notebook JSON, or has no ``cells`` list
    * a code cell has a committed error output (a traceback was saved)

warnings (reported, do not fail)
    * the notebook contains no code cells at all
    * a source line embeds an absolute local path such as /Users/<name>/...,
      which will not exist on anyone else's machine
    * the notebook is unusually large, which normally means huge embedded
      outputs that bloat every future clone

Usage
-----
    python .github/scripts/check_notebooks.py                 # scan everything
    python .github/scripts/check_notebooks.py --changed-files a.ipynb b.ipynb
    CHANGED_FILES="a.ipynb b.ipynb" python .github/scripts/check_notebooks.py
"""

import argparse
import json
import os
import re
import sys
import uuid
from pathlib import Path

# Absolute paths that only exist on the author's machine.
LOCAL_PATH_PATTERNS = (
    re.compile(r"/Users/[A-Za-z0-9._-]+/"),
    re.compile(r"/home/[A-Za-z0-9._-]+/"),
    re.compile(r"[A-Za-z]:\\\\Users\\\\", re.IGNORECASE),
    re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
)

# Paths that are fine to reference even though they look absolute.
LOCAL_PATH_ALLOWLIST = ("/home/user/", "/Users/runner/")

LARGE_NOTEBOOK_MB = 5.0


def emit(level, message):
    """Print a message, as a GitHub annotation when running in Actions."""
    if os.getenv("GITHUB_ACTIONS") == "true":
        print(f"::{level}::{message}")
    else:
        print(f"{level.upper()}: {message}")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Statically validate notebooks.")
    parser.add_argument("--root-dir", default=".", help="Repository root to scan.")
    parser.add_argument(
        "--changed-files",
        nargs="*",
        default=None,
        help="Restrict the scan to these files.",
    )
    return parser.parse_args(argv)


def normalize_changed_files(entries):
    """Split whitespace or newline separated paths into a flat list."""
    paths = []
    for entry in entries or []:
        if not entry:
            continue
        paths.extend(part for part in re.split(r"\s+", entry.strip()) if part)
    return paths


def find_notebooks(root_dir=".", changed_files=None):
    """Return the notebooks to check, preferring an explicit changed-file list."""
    root = Path(root_dir).resolve()
    entries = normalize_changed_files(changed_files)

    from_env = os.getenv("CHANGED_FILES", "")
    if from_env and "No changed files detected" not in from_env:
        entries.extend(normalize_changed_files([from_env]))

    if entries:
        notebooks = []
        for entry in entries:
            candidate = Path(entry)
            if not candidate.is_absolute():
                candidate = (root / candidate).resolve()
            if (
                candidate.is_file()
                and candidate.suffix.lower() == ".ipynb"
                and ".ipynb_checkpoints" not in str(candidate)
            ):
                notebooks.append(candidate)
        return sorted(dict.fromkeys(notebooks))

    return sorted(
        path
        for path in root.rglob("*.ipynb")
        if ".ipynb_checkpoints" not in str(path)
    )


def cell_source(cell):
    """Return a cell's source as one string, whatever shape it is stored in."""
    source = cell.get("source", [])
    if isinstance(source, list):
        return "".join(source)
    return source if isinstance(source, str) else ""


def find_local_paths(text):
    """Return absolute machine-specific paths referenced in ``text``."""
    hits = []
    for pattern in LOCAL_PATH_PATTERNS:
        for match in pattern.findall(text):
            if not any(match.startswith(allowed) for allowed in LOCAL_PATH_ALLOWLIST):
                hits.append(match)
    return hits


def check_notebook(path):
    """Return ``(errors, warnings)`` for a single notebook."""
    errors, warnings = [], []
    name = Path(path).name

    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{name}: not valid notebook JSON ({exc})"], []
    except OSError as exc:
        return [f"{name}: could not be read ({exc})"], []

    cells = payload.get("cells")
    if not isinstance(cells, list):
        return [f"{name}: no 'cells' list - this is not a valid notebook"], []
    if not cells:
        return [f"{name}: contains no cells"], []

    size_mb = Path(path).stat().st_size / (1024 * 1024)
    if size_mb > LARGE_NOTEBOOK_MB:
        warnings.append(
            f"{name}: {size_mb:.1f} MB is large; consider clearing bulky outputs "
            f"before committing"
        )

    code_cells = 0
    for index, cell in enumerate(cells, start=1):
        if cell.get("cell_type") == "code":
            code_cells += 1
            for output in cell.get("outputs") or []:
                if output.get("output_type") == "error":
                    ename = output.get("ename", "Error")
                    errors.append(
                        f"{name}: cell {index} has a committed {ename} traceback - "
                        f"re-run the cell and save a clean output"
                    )

        for local_path in find_local_paths(cell_source(cell)):
            warnings.append(
                f"{name}: cell {index} references the local path '{local_path}...' "
                f"which will not exist for other users"
            )

    if code_cells == 0:
        warnings.append(f"{name}: contains no code cells")

    return errors, warnings


def build_report(results):
    """Render a Markdown summary of every notebook that was checked."""
    total_errors = sum(len(item["errors"]) for item in results)
    total_warnings = sum(len(item["warnings"]) for item in results)

    lines = ["### 📓 Notebook Quality Check"]
    if not results:
        lines.append("\nNo notebooks were changed. Nothing to check. 🎉")
        return "\n".join(lines)

    lines.append(f"\n**Notebooks checked:** {len(results)}")
    lines.append(f"**Errors:** {total_errors} · **Warnings:** {total_warnings}\n")

    if total_errors:
        lines.append("#### ❌ Errors")
        for item in results:
            lines.extend(f"- {message}" for message in item["errors"])
    if total_warnings:
        lines.append("\n#### ⚠️ Warnings")
        for item in results:
            lines.extend(f"- {message}" for message in item["warnings"])
    if not total_errors and not total_warnings:
        lines.append("All changed notebooks look clean. 🎉")

    return "\n".join(lines)


def write_github_output(report):
    """Expose the report to later workflow steps."""
    target = os.environ.get("GITHUB_OUTPUT")
    if not target:
        return
    delimiter = str(uuid.uuid4())
    with open(target, "a", encoding="utf-8") as handle:
        handle.write(f"report<<{delimiter}\n{report}\n{delimiter}\n")


def run(root_dir=".", changed_files=None):
    """Check the selected notebooks and return the number of hard errors."""
    notebooks = find_notebooks(root_dir, changed_files)
    if not notebooks:
        print("No notebooks to check.")
        write_github_output(build_report([]))
        return 0

    print(f"Checking {len(notebooks)} notebook(s)...")
    results = []
    for notebook in notebooks:
        errors, warnings = check_notebook(notebook)
        results.append({"path": str(notebook), "errors": errors, "warnings": warnings})
        for message in errors:
            emit("error", message)
        for message in warnings:
            emit("warning", message)
        if not errors and not warnings:
            print(f"  ok  {Path(notebook).name}")

    report = build_report(results)
    write_github_output(report)

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write(report + "\n")
    else:
        print("\n" + report)

    return sum(len(item["errors"]) for item in results)


def main(argv=None):
    args = parse_args(argv)
    return 1 if run(args.root_dir, args.changed_files) else 0


if __name__ == "__main__":
    sys.exit(main())
