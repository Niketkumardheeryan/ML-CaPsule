'''

This short program utilizes the tools of requests and beautiful soup in order to web scrape information from the
products page of Newegg and parses it into a useful CSV data file for analysis.

'''

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def get_html(url):
    '''
        Accepts a single URL argument and makes an HTTP GET request to that URL. If nothing goes wrong and
        the content-type of the response is some kind of HTMl/XML, return the raw HTML content for the
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

def get_products():
    ''' 
        Downloads the webpage, iterates over <div> elements and picks out the brand, product name, product
        price and shipping costs into a list.
    '''
    url = "https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=graphics+cards&N=-1&isNodeId=1"
    response = get_html(url)

    items_desc = []
    if response is not None:
        soup = BeautifulSoup(response, "html.parser")
        products = soup.find_all("div", {"class": "item-container"})
        for product in products:
            brand = product.div.div.a.img["title"]
            
            product_name = product.find("a", {"class": "item-title"}).text.strip()
            
            product_price = product.find("li", {"class": "price-current"})
            full_price = product_price.strong.text + product_price.sup.text

            shipping = product.find("li", {"class": "price-ship"}).text.strip()

            items_desc.append((brand, product_name, full_price, shipping))
        return items_desc
    raise Exception(f"There was an error retrieving contents at {url}")

def write_products(item_desc):
    ''' 
        Accepts a single item list as an argument, proceses through the list and writes all the products into
        a single CSV data file.
    '''
    headers = "brand, product_name, product_price, shipping\n"
    filename = "products.csv"
    try: 
        f = open(filename, "w")
        f.write(headers)
        for brand, product_name, product_price, shipping in item_desc:
            f.write(brand.replace(","," ") + "," + product_name.replace(",", "|") + ",$" + product_price + "," + shipping + "\n")
        f.close()
    except:
        print("There was an error writing to the CSV data file.")
    
if __name__ == "__main__":
    '''

        1. Get list of products with brand name, product name, product price and shipping costs.
        2. Iterate over list of products to write data into a CSV file.

    '''
    print("Getting list of products and descriptions...")
    item_desc = get_products()
    print("...done\n")

    print("Writing product information to a CSV file...")
    write_products(item_desc)
    print("...done\n")