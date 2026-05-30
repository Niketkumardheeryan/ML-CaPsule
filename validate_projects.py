from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".github",
    ".idea",
    "__pycache__"
}

root = Path.cwd()

total_projects = 0
passed_projects = 0
failed_projects = 0

print("\n=== ML-CaPsule Project Validation Report ===\n")

for project in root.iterdir():

    if not project.is_dir():
        continue

    if project.name in SKIP_DIRS:
        continue

    issues = []

    # Check README.md (case-insensitive)
    has_readme = any(
        file.is_file() and file.name.lower() == "readme.md"
        for file in project.iterdir()
    )

    # Check requirements.txt (case-insensitive)
    has_requirements = any(
        file.is_file() and file.name.lower() == "requirements.txt"
        for file in project.iterdir()
    )

    # Check for Python scripts or notebooks anywhere in the project
    has_code = any(
        file.suffix.lower() in [".py", ".ipynb"]
        for file in project.rglob("*")
        if file.is_file()
    )

    if not has_readme:
        issues.append("Missing README.md")

    if not has_requirements:
        issues.append("Missing requirements.txt")

    if not has_code:
        issues.append("No .py or .ipynb file found")

    total_projects += 1

    if issues:
        failed_projects += 1
        print(f"{project.name}")
        for issue in issues:
            print(f"   - {issue}")
        print()
    else:
        passed_projects += 1
        print(f" {project.name}")

print("\n" + "=" * 50)
print("Validation Summary")
print("=" * 50)
print(f"Total Projects Checked : {total_projects}")
print(f"Passed                 : {passed_projects}")
print(f"Failed                 : {failed_projects}")
print("=" * 50)