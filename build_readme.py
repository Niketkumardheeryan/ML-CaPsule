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
	req = requests.get(FEED_URL)
	soup = BeautifulSoup(req.text, 'html.parser')
	temp=[]
	li = soup.findAll('div', class_="Box-row Box-row--focus-gray py-2 d-flex position-relative js-navigation-item")
	for i in li:
		for x in i.findAll('a',class_="js-navigation-open Link--primary"):
			if(x.text!=".github" and x.text!="CODE_OF_CONDUCT.md" and x.text!="CONTRIBUTING_GUIDELINES.md" and x.text!=".github/workflows" and x.text!="build_readme.py" and x.text!="requirements.txt" and x.text!="README.md" and x.text!="download statistics.jpg" and x.text!="img" and x.text!="ml img.jpg"):
				temp2={
                	'fname' : x.text,
                	'furl': x["href"].split('/')[-1]
				   		}
				temp.append(temp2)
			else:pass
	return temp


if __name__ == "__main__":
    readme = ROOT_PATH / "README.md"
    readme_contents = readme.open().read()

    file_names = Exract_files_names()
    file_md="\n\n".join(["- {}".format(i) for i in file_names])
    file_md = "\n\n".join(
        ["- [{fname}]({furl})".format(**i) for i in file_names]
    )

    readme_contents = replace_chunk(readme_contents, "Projects", file_md)
    readme.open("w").write(readme_contents)


