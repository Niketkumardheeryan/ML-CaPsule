from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup  # You will need to run: pip install beautifulsoup4
import sys

ROOT_PATH = Path(__file__).parent.resolve()

# Add your GitHub repository URL here
FEED_URL = "https://github.com/Niketkumardheeryan/ML-CaPsule"

EXCLUDED_NAMES = {
    ".github",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING_GUIDELINES.md",
    ".github/workflows",
    "build_readme.py",
    "requirements.txt",
    "README.md",
    "download statistics.jpg",
    "img",
    "ml img.jpg",
    ".git",
    "__pycache__",
}

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

def extract_file_names():
    temp = []

    # 1. Fetch the HTML from GitHub
    try:
        req = requests.get(FEED_URL, timeout=10)
        req.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("ERROR: Failed to fetch repository data: {}".format(e))
        sys.exit(1)

    # 2. Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(req.text, "html.parser")

    # 3. Define the missing 'li' variable. 
    # Wrapping soup in a list allows your existing 'for i in li:' loop to work perfectly.
    li = [soup] 

    # 4. Your existing loop
    for i in li:
        for x in i.findAll('a', class_="js-navigation-open Link--primary"):
            if (x.text not in EXCLUDED_NAMES): # Streamlined your exclusion list check
                temp2 = {
                    'fname': x.text,
                    # Grabs the actual file/folder name from the end of the URL
                    'furl': x["href"].split('/')[-1].replace(" ", "%20") 
                }
                temp.append(temp2)
    return temp

if __name__ == "__main__":
    readme = ROOT_PATH / "README.md"

    if not readme.exists():
        print(f"ERROR: {readme} not found.")
        sys.exit(1)

    with open(readme, "r", encoding="utf-8") as readme_file:
        readme_contents = readme_file.read()

    file_names = extract_file_names()

    file_md = "\n".join(
        ["| [{fname}]({furl}) |".format(**i) for i in file_names]
    )

    updated_content = replace_chunk(
        readme_contents,
        "Projects",
        "| Content List |\n| --------------- |\n" + file_md,
    )

    with open(readme, "w", encoding="utf-8") as readme_file:
        readme_file.write(updated_content)

    print("README.md updated successfully.")