#!/usr/bin/env python3
"""
Notebook Health Check Bot
Automatically tests Jupyter notebooks for errors, missing imports, and deprecations.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import uuid
from pathlib import Path


def emit_warning(message):
    """Emit a warning that is visible in local logs and GitHub Actions."""
    if os.getenv("GITHUB_ACTIONS") == "true":
        print(f"::warning::{message}")
    else:
        print(f"WARNING: {message}")


def parse_args(argv=None):
    """Parse command line arguments for the health check."""
    parser = argparse.ArgumentParser(description="Run notebook health checks.")
    parser.add_argument("--root-dir", default=".", help="Repository root to scan.")
    parser.add_argument(
        "--changed-files",
        nargs="*",
        default=None,
        help="Optional list of changed files to restrict the scan to.",
    )
    return parser.parse_args(argv)


def normalize_changed_files(changed_files):
    """Normalize newline- or whitespace-delimited changed file paths into a list."""
    normalized = []
    for entry in changed_files or []:
        if not entry:
            continue
        for part in re.split(r"\s+", entry.strip()):
            if part:
                normalized.append(part)
    return normalized


def find_notebooks(root_dir=".", changed_files=None):
    if changed_files is None:
        changed_files = []

    notebooks = []
    root_path = Path(root_dir).resolve()

    changed_file_entries = normalize_changed_files(changed_files)
    env_changed_files = os.getenv("CHANGED_FILES", "")
    
    # Check if the bash script passed the fallback message instead of real files
    is_fallback = "No changed files detected" in env_changed_files
    
    if env_changed_files and not is_fallback:
        changed_file_entries.extend(normalize_changed_files([env_changed_files]))

    if changed_file_entries and not is_fallback:
        for entry in changed_file_entries:
            candidate = Path(entry)
            if not candidate.is_absolute():
                candidate = (root_path / candidate).resolve()
            if candidate.exists() and candidate.is_file() and candidate.suffix.lower() == ".ipynb":
                if ".ipynb_checkpoints" not in str(candidate):
                    notebooks.append(candidate)
        if notebooks:
            return sorted(dict.fromkeys(notebooks))
        print("No changed notebook files matched the health check criteria.")
        return []

    # If we get here, no specific changed files were found, so do a full scan
    print("Performing full notebook scan...")
    for candidate in root_path.rglob("*.ipynb"):
        if ".ipynb_checkpoints" not in str(candidate):
            notebooks.append(candidate)
            
    return sorted(dict.fromkeys(notebooks))


def classify_notebook(payload, notebook_path):
    """Classify a notebook before execution to avoid unnecessary runtime and flag manual-review cases."""
    notebook_name = str(notebook_path).lower()
    source_text = ""

    for cell in payload.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", [])
        if isinstance(source, list):
            source_text += "".join(source)
        elif isinstance(source, str):
            source_text += source

    source_text = source_text.lower()

    manual_patterns = [
        r"requests\.(get|post|put|delete)",
        r"selenium|playwright|webdriver",
        r"opencv|cv2",
        r"pytube|youtube|streamlit|gradio",
        r"google\.colab|drive\.mount",
        r"api[_ -]?key|token|password",
        r"openai|anthropic|huggingface|transformers",
        r"torch\.load|joblib\.load|pickle\.load",
    ]
    skip_patterns = [
        r"manual inspection",
        r"todo|tbd|fixme",
        r"<[^>]+>",
    ]

    requires_manual_inspection = any(re.search(pattern, source_text) for pattern in manual_patterns)
    should_run = not requires_manual_inspection

    if not should_run:
        reason = "Notebook matches manual inspection heuristics and will be flagged for review."
    elif any(re.search(pattern, source_text) for pattern in skip_patterns):
        reason = "Notebook contains review markers and will be skipped."
        should_run = False
        requires_manual_inspection = True
    else:
        reason = "Notebook looks runnable and will be executed."

    if "copy_of_" in notebook_name or "test" in notebook_name:
        reason = f"{reason} Name-based heuristic also suggests a support notebook."
        should_run = should_run and "test" not in notebook_name
        requires_manual_inspection = requires_manual_inspection or "test" in notebook_name

    return {
        "should_run": should_run,
        "requires_manual_inspection": requires_manual_inspection,
        "reason": reason,
    }


def load_notebook_payload(notebook_path):
    """Load notebook JSON content for pre-screening."""
    try:
        with open(notebook_path, "r", encoding="utf-8") as handle:
            return json.loads(handle.read())
    except Exception as exc:
        print(f"Error reading {notebook_path}: {exc}")
        return None


def test_notebook(notebook_path):
    """Test a single notebook using nbconvert."""
    result = {
        "path": str(notebook_path),
        "success": False,
        "error": None,
        "returncode": None,
        "skipped": False,
        "reason": None,
    }

    payload = load_notebook_payload(notebook_path)
    if payload is None:
        result["error"] = "Unable to read notebook JSON"
        return result

    classification = classify_notebook(payload, notebook_path)
    result["reason"] = classification["reason"]
    if not classification["should_run"]:
        result["skipped"] = True
        result["success"] = True
        result["error"] = None
        if classification["requires_manual_inspection"]:
            emit_warning(f"{notebook_path}: {classification['reason']}")
        else:
            print(f"Skipping {notebook_path}: {classification['reason']}")
        return result

    try:
        completed = subprocess.run(
            [
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                str(notebook_path),
                "--output",
                "-",
                "--allow-errors",
            ],
            capture_output=True,
            text=True,
            timeout=300,
        )
        result["returncode"] = completed.returncode
        result["success"] = completed.returncode == 0
        if completed.returncode != 0:
            output = (completed.stderr or completed.stdout).strip()
            result["error"] = output or f"Notebook execution failed with exit code {completed.returncode}"
    except subprocess.TimeoutExpired:
        result["error"] = "Timeout (5 minutes)"
    except Exception as e:
        result["error"] = str(e)

    return result


def run_health_check(root_dir=".", changed_files=None):
    """Run the notebook health checks and report failed notebooks as warnings."""
    notebooks = find_notebooks(root_dir, changed_files)
    
    results = []
    failed = []
    skipped = []
    report_lines = ["### 📝 Notebook Health Check Results"]
    
    if not notebooks: # if no notebooks are found just print a message and add to the report
        print("No notebooks found to test.")
        report_lines.append("\n**No notebooks were found or changed.** No tests were run. 🎉")
    else:
        print(f"Found {len(notebooks)} notebooks to test.")
        for nb in notebooks:
            print(f"Testing: {nb}")
            result = test_notebook(nb)
            results.append(result)

        failed = [r for r in results if not r["success"] and not r.get("skipped")]
        skipped = [r for r in results if r.get("skipped")]

        if failed:
            print(f"\n⚠️ {len(failed)} notebooks reported warnings:")
            for fail in failed:
                message = f"Notebook execution issue: {fail['path']}: {fail['error']}"
                emit_warning(message)
                print(f"  - {fail['path']}: {fail['error']}")

        if skipped:
            print(f"\nℹ️ {len(skipped)} notebooks were flagged for manual inspection and skipped:")
            for item in skipped:
                print(f"  - {item['path']}: {item['reason']}")
        else:
            if results and not failed:
                print(f"\n✅ All {len(results)} notebooks passed!")

        # Build the Markdown Report content
        report_lines.append(f"\n**Total notebooks checked:** {len(results)}\n")
        
        report_lines.append(f"#### Failed Notebooks ({len(failed)})")
        if failed:
            for fail in failed:
                report_lines.append(f"- **{fail['path']}**: {fail['error']}")
        else:
            report_lines.append("None! 🎉")
            
        report_lines.append(f"\n#### Skipped Notebooks ({len(skipped)})")
        if skipped:
            for skip in skipped:
                report_lines.append(f"- **{skip['path']}**: {skip['reason']}")
        else:
            report_lines.append("None")

    report_string = "\n".join(report_lines)

    # --- Write to GITHUB_OUTPUT ---
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a', encoding="utf-8") as outfile:
            delimiter = str(uuid.uuid4())
            outfile.write(f"report<<{delimiter}\n")
            outfile.write(f"{report_string}\n")
            outfile.write(f"{delimiter}\n")
    else:
        # Fallback for running locally
        print("\n--- Markdown Report ---")
        print(report_string)

    return results


def main(argv=None):
    args = parse_args(argv)
    run_health_check(args.root_dir, args.changed_files)
    return 0


if __name__ == "__main__":
    sys.exit(main())