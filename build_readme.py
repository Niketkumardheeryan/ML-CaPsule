from pathlib import Path
import re

ROOT_PATH = Path(__file__).parent.resolve()

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

def Exract_files_names():
    try:
        req = requests.get(FEED_URL, timeout=10)
        req.raise_for_status()
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out. GitHub may be rate-limiting or unreachable.")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print("ERROR: HTTP error occurred: {}".format(e))
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("ERROR: Failed to connect. Check your internet connection.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print("ERROR: An unexpected error occurred: {}".format(e))
        sys.exit(1)

def extract_file_names():
    temp = []

    for path in sorted(ROOT_PATH.iterdir(), key=lambda item: item.name.casefold()):
        if not path.is_dir():
            continue

        if path.name in EXCLUDED_NAMES or path.name.startswith("."):
            continue

        temp.append(
            {
                "fname": path.name,
                "furl": path.name,
            }
        )

    return temp

    for i in li:
        for x in i.findAll('a', class_="js-navigation-open Link--primary"):
            if (x.text != ".github" and x.text != "CODE_OF_CONDUCT.md" and x.text != "CONTRIBUTING_GUIDELINES.md" and x.text != ".github/workflows" and x.text != "build_readme.py" and x.text != "requirements.txt" and x.text != "README.md" and x.text != "download statistics.jpg" and x.text != "img" and x.text != "ml img.jpg"):
                temp2 = {
                    'fname': x.text,
                    'furl': x["href"].split('/')[-1]
                }
                temp.append(temp2)
    return temp

if __name__ == "__main__":

    readme = ROOT_PATH / "README.md"

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