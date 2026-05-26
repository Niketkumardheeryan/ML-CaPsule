import requests
from bs4 import BeautifulSoup
import pathlib
import re


ROOT_PATH = pathlib.Path(__file__).parent.resolve()
FEED_URL = 'https://github.com/Niketkumardheeryan/Hands-on-ML-Basic-to-Advance-'

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} start \-\->.*<!\-\- {} end \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} start -->{}<!-- {} end -->".format(marker, chunk, marker)
    return r.sub(chunk, content)



def Exract_files_names():
    temp = []
    ignored = {
        ".git", ".github", ".ipynb_checkpoints", "__pycache__", "venv", ".venv",
        "CODE_OF_CONDUCT.md", "CONTRIBUTING_GUIDELINES.md", "CONTRIBUTING.md", "ROADMAP.md",
        "build_readme.py", "requirements.txt", "README.md", "download statistics.jpg",
        "img", "ml img.jpg", "website", ".DS_Store", "LICENSE", "Sql"
    }
    for path in sorted(ROOT_PATH.iterdir(), key=lambda p: p.name.lower()):
        name = path.name
        if name in ignored or name.startswith('.'):
            continue
        temp.append({
            'fname': name,
            'furl': name.replace(' ', '%20')
        })
    return temp


if __name__ == "__main__":
    readme = ROOT_PATH / "README.md"
    readme_contents = readme.open(encoding="utf-8").read()

    file_names = Exract_files_names()
    file_md="\n\n".join(["- {}".format(i) for i in file_names])
    file_md = "\n".join(
        ["| [{fname}]({furl}) |".format(**i) for i in file_names]
    )

    
    readme_contents = replace_chunk(readme_contents, "Projects", "| Content List | \n | --------------- | \n" + file_md)
    readme.open("w", encoding="utf-8").write(readme_contents)


