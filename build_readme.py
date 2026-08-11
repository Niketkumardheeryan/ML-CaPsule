from pathlib import Path
import re
import sys

ROOT_PATH = Path(__file__).parent.resolve()

EXCLUDED_NAMES = {
    ".github",
    ".git",
    "__pycache__",
    "README.md",
    "build_readme.py",
    "requirements.txt",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "CONTRIBUTING_GUIDELINES.md",
    "LICENSE",
    ".gitignore",
    ".DS_Store",
    "ROADMAP.md",
    "img",
    "ml img.jpg",
    "download statistics.jpg",
}


def replace_chunk(content, marker, chunk):
    pattern = re.compile(
        rf"<!-- {marker} start -->.*<!-- {marker} end -->",
        re.DOTALL,
    )

    replacement = (
        f"<!-- {marker} start -->\n"
        f"{chunk}\n"
        f"<!-- {marker} end -->"
    )

    if pattern.search(content):
        return pattern.sub(replacement, content)

    # Marker missing → append section instead
    return (
        content.rstrip()
        + "\n\n"
        + replacement
        + "\n"
    )


def infer_project_metadata(project_name):
    name = project_name.lower()

    advanced_keywords = (
        "gan",
        "transformer",
        "reinforcement learning",
        "reinforcement",
        "rl",
        "llm",
        "genetic",
        "trading",
        "optimization",
        "deepfake",
        "yolo",
        "stitching",
        "captioning",
        "generator",
        "virtual drag",
    )

    beginner_keywords = (
        "basics",
        "python",
        "power bi",
        "cheat sheets",
        "statistics",
        "eda",
        "pandas",
        "numpy",
        "sql",
        "data cleaning",
        "data filling",
        "visualization",
        "plot",
        "matplotlib",
        "seaborn",
    )

    if any(keyword in name for keyword in advanced_keywords):
        return "🟠 Advanced", "6-12 hours"

    if any(keyword in name for keyword in beginner_keywords):
        return "🟢 Beginner", "1-3 hours"

    return "🟡 Intermediate", "3-6 hours"


def build_project_table(projects):
    headers = [
        "| Project | Difficulty | Estimated Time |",
        "|---------|------------|----------------|",
    ]

    rows = []
    for project in projects:
        difficulty, time_estimate = infer_project_metadata(project["fname"])
        rows.append(
            f"| [{project['fname']}]({project['furl']}) | {difficulty} | {time_estimate} |"
        )

    return "\n".join(headers + rows)


def extract_file_names():
    projects = []

    for path in sorted(ROOT_PATH.iterdir(), key=lambda item: item.name.lower()):
        if path.is_dir() and path.name not in EXCLUDED_NAMES:
            projects.append(
                {
                    "fname": path.name,
                    "furl": path.name.replace(" ", "%20"),
                }
            )

    projects.sort(key=lambda x: x["fname"].lower())

    return projects


def main():
    readme = ROOT_PATH / "README.md"

    if not readme.exists():
        print("README.md not found.")
        sys.exit(1)

    with open(readme, "r", encoding="utf-8") as f:
        readme_contents = f.read()

    projects = extract_file_names()

    table = build_project_table(projects)
    section = (
        "<details>\n"
        "<summary><b>🧭 Suggested Learning Path</b> — Click to expand</summary>\n\n"
        "<br>\n\n"
        "Start with beginner-friendly projects, then move to intermediate and advanced ones as your confidence grows. "
        "The table below adds quick difficulty and time guidance for each project.\n\n"
        f"{table}\n"
        "</details>"
    )

    updated = replace_chunk(
        readme_contents,
        "Projects",
        section,
    )

    with open(readme, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"README updated with {len(projects)} projects.")


if __name__ == "__main__":
    main()