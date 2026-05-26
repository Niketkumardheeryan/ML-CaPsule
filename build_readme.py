import pathlib
import re

ROOT_PATH = pathlib.Path(__file__).parent.resolve()

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} start \-\->.*<!\-\- {} end \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} start -->{}<!-- {} end -->".format(marker, chunk, marker)
    return r.sub(chunk, content)


def extract_file_names():
    exclude_list = {
        ".git", ".github", ".idea", "__pycache__", "CODE_OF_CONDUCT.md", 
        "CONTRIBUTING_GUIDELINES.md", "build_readme.py", "requirements.txt", 
        "README.md", "download statistics.jpg", "img", "ml img.jpg"
    }
    
    temp = []
    for path in sorted(ROOT_PATH.iterdir()):
        if path.name not in exclude_list and not path.name.startswith('.'):
            # Encode URL properly if needed, but for simplicity we keep the original format
            temp.append({
                'fname': path.name,
                'furl': path.name.replace(" ", "%20")
            })
    return temp


if __name__ == "__main__":
    readme = ROOT_PATH / "README.md"
    readme_contents = readme.open("r", encoding="utf-8").read()

    file_names = extract_file_names()
    file_md = "\n".join(
        ["| [{fname}]({furl}) |".format(**i) for i in file_names]
    )

    readme_contents = replace_chunk(readme_contents, "Projects", "| Content List | \n | --------------- | \n" + file_md)
    readme.open("w", encoding="utf-8").write(readme_contents)
