'''

This short program utilizes the tools of requests, context library and beautiful soup in order to download a list 
of 100 mathematicians and their XTools page, selects data about their popularity and finish by producing the top 
5 most popular mathematicians of all time.

'''

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
 
def get_html(url):
    '''
        Accepts a single URL argument and makes an HTTP GET request to that URL. If nothing goes wrong and
        the content-type of the response is some kind of HTML/XML, return the raw HTML content for the 
        requested page. However, if there were problems with the request, return None.
    ''' 
    try:
        with closing(get(url, stream=True)) as resp:
            if quality_response(resp):
                return resp.content
            else:
                return None
    except RequestException as re:
        print(f"There was an error during requests to {url} : {str(re)}")
        return None
    
def quality_response(resp):
    '''
        Returns true if response seems to be HTML, false otherwise.
    '''
    content_type = resp.headers["Content-Type"].lower()
    return (resp.status_code == 200 and content_type is not None and content_type.find("html") > - 1)

def get_names():
    '''
        Downloads the webpage, iterates over <li> elements and picks out each name that occurs into a set
        which ensures no duplicate names. Convert the set into a list and return it.
    '''
    url = "http://www.fabpedigree.com/james/mathmen.htm"
    response = get_html(url)

    if response is not None:
        soup = BeautifulSoup(response, "html.parser")
        names = set()
        for li in soup.select("li"):
            for name in li.text.split("\n"):
                if len(name) > 0:
                    names.add(name.strip())
        return list(names)
    raise Exception(f"There was an error retrieving contents at {url}")

def get_hits(name):
    '''
        Accepts a single name argument and returns the number of hits that mathematician wiki page received
        in the last 60 days as an INT.
    '''
    base_url = "https://xtools.wmflabs.org/articleinfo/en.wikipedia.org/{}"
    response = get_html(base_url.format(name))

    if response is not None:
        soup = BeautifulSoup(response, "html.parser")

        hit_link = [ hl for hl in soup.select("a") if hl["href"].find("latest-60") > -1 ]
        if len(hit_link) > 0:
            text = hit_link[0].text.replace(",", "")
            try:
                return int(text)
            except:
                print(f"Could not parse {text} as an INT.")
    print(f"No page views found for {name}.")
    return None

if __name__ == "__main__":
    '''

        1. Get a list of names.
        2. Iterate over the list of names to get a popularity score for each name.
        3. Print out the names, sorted by popularity.
        4. Track instances in which there are no popularity scores and print message showing the number of
           thoes left out of rankings.

    '''
    print("Getting the list of names...")
    names = get_names()
    print("...done\n")

    results = []

    print("Getting the stats for each name...")
    for name in names:
        try:
            hit = get_hits(name)
            if hit is None:
                hit = -1
            results.append((hit, name))
        except:
            results.append((-1, name))
            print(f"There was an error while processing {name}, so we are skipping...")
            
    print("...done\n")

    results.sort()
    results.reverse()

    if len(results) > 5: 
        most_popular = results[:5]
    else:
        most_popular = results
    
    print("\n The Most Popular Mathematicians are: \n")
    for (mark, mathematician) in most_popular:
        print(f"{mathematician} with {mark} page views.")
    
    failed_results = len([fr for fr in results if fr[0] == -1])
    print(f"\nWe were unable to find results for {failed_results} mathematician(s) on our list.")