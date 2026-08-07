from pathlib import Path
import re
import requests
import sys

ROOT_PATH = Path(__file__).parent.resolve()

API_URL = "https://api.github.com/repos/Niketkumardheeryan/ML-CaPsule/contents?per_page=1000"

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


def extract_file_names():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    items = response.json()

    projects = []

    for item in items:
        if (
            item["type"] == "dir"
            and item["name"] not in EXCLUDED_NAMES
        ):
            projects.append(
                {
                    "fname": item["name"],
                    "furl": item["path"].replace(" ", "%20"),
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

    table = [
        "| Content List |",
        "|---------------|",
    ]

    table.extend(
        [
            f"| [{p['fname']}]({p['furl']}) |"
            for p in projects
        ]
    )

    updated = replace_chunk(
        readme_contents,
        "Projects",
        "\n".join(table),
    )

    with open(readme, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"README updated with {len(projects)} projects.")


if __name__ == "__main__":
    main()