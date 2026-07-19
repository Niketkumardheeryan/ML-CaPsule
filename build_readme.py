#!/usr/bin/env python3
import json
import re
from pathlib import Path
import sys

ROOT_PATH = Path(__file__).parent.resolve()
INDEX_FILE = ROOT_PATH / "project-index.json"
README_FILE = ROOT_PATH / "README.md"

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} start \-\->.*<!\-\- {} end \-\->".format(marker, marker),
        re.DOTALL,
    )

    if not inline:
        chunk = "\n{}\n".format(chunk)

    chunk = "<!-- {} start -->{}<!-- {} end -->".format(
        marker,
        chunk,
        marker,
    )

    return r.sub(chunk, content)

def build_readme_table():
    if not INDEX_FILE.exists():
        print(f"ERROR: {INDEX_FILE} not found. Run generate-project-index.py first.")
        sys.exit(1)
        
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        projects = json.load(f)

    headers = "| S.No | Project | S.No | Project | S.No | Project | S.No | Project |"
    separator = "|:----:|---------|:----:|---------|:----:|---------|:----:|---------|"
    
    rows = [headers, separator]
    num_cols = 4
    
    for i in range(0, len(projects), num_cols):
        row_cells = []
        for j in range(num_cols):
            idx = i + j
            if idx < len(projects):
                proj = projects[idx]
                encoded_path = proj['path'].replace(" ", "%20")
                url = f"https://github.com/Niketkumardheeryan/ML-CaPsule/tree/master/{encoded_path}"
                row_cells.append(f" {idx + 1} ")
                row_cells.append(f" [{proj['name']}]({url}) ")
            else:
                row_cells.append(" ")
                row_cells.append(" ")
        rows.append("|" + "|".join(row_cells) + "|")
        
    return "\n".join(rows)

if __name__ == "__main__":
    if not README_FILE.exists():
        print(f"ERROR: {README_FILE} not found.")
        sys.exit(1)

    with open(README_FILE, "r", encoding="utf-8") as readme_file:
        readme_contents = readme_file.read()

    table_md = build_readme_table()

    updated_content = replace_chunk(
        readme_contents,
        "Projects",
        table_md,
    )

    with open(README_FILE, "w", encoding="utf-8") as readme_file:
        readme_file.write(updated_content)

    print("README.md updated successfully with the auto-generated project index table.")