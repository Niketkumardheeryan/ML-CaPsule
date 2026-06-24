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
}

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} start \-\->.*<!\-\- {} end \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} start -->{}<!-- {} end -->".format(marker, chunk, marker)
    return r.sub(chunk, content)

def Extract_file_names():
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


if __name__ == "__main__":
    readme = ROOT_PATH / "README.md"
    with open(readme, "r", encoding="utf-8") as readme_file:
        readme_contents = readme_file.read()

    file_names = Extract_file_names()
    file_md = "\n".join(
        ["| [{fname}]({furl}) |".format(**i) for i in file_names]
    )

    
    readme_contents = replace_chunk(readme_contents, "Projects", "| Content List | \n | --------------- | \n" + file_md)
    with open(readme, "w", encoding="utf-8") as readme_file:
        readme_file.write(readme_contents)


