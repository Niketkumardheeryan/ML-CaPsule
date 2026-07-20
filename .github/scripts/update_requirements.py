from pathlib import Path
import re
import sys

ROOT_PATH = Path(".")

global_requirements_path = ROOT_PATH / "requirements.txt"

def check_requirements_file(requirements_path): 
    """
    Check if the requirements.txt file exists and is not empty.
    """
    if not requirements_path.exists() or requirements_path.stat().st_size == 0:
        return False
    return True

def find_all_requirements_files(root_path):
    """
    Recursively find all requirements.txt files in the given root path.
    """
    return set(root_path.rglob("requirements.txt"))


def parse_requirements(file_path: str) -> dict[str, str]:
    """
    Parses a requirements.txt file into a dictionary of {package: version}.
    """
    requirements = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Strip whitespace and remove inline comments
            line = line.split('#')[0].strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Split on the first version specifier (==, >=, <=, ~=, >, <)
            parts = re.split(r'([=<>~]+)', line, maxsplit=1)
            
            package = parts[0].strip()
            
            # If a version specifier exists, join the operator and the version
            if len(parts) > 1:
                version = "".join(parts[1:]).strip()
                # Remove environment markers (e.g., ; python_version < "3.8")
                version = version.split(';')[0].strip()
            else:
                version = "any" # No version specified
            
            requirements[package] = version
            
    return requirements

def update_requirements():
    """
    Update the README.md file with the contents of all requirements.txt files.
    """
    files = find_all_requirements_files(ROOT_PATH)

    requirements_data = {}

    for file in files:
        if check_requirements_file(file):
            reqs = parse_requirements(file)
            for package , version in reqs.items():
                if package not in requirements_data.keys():
                    requirements_data[package] = version
                if requirements_data[package] < version:
                    requirements_data[package] = version

    
    try:            
        with open(global_requirements_path, 'w') as f:
            for package, version in sorted(requirements_data.items()):
                f.write(f"{package}=={version}\n")
    except Exception as e:
        print(f"Error writing to {global_requirements_path}: {e}")
        sys.exit(1)




        