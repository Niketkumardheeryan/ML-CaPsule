'''

This short program utilizes the tools of requests, beautiful soup, context library, datetime and csv in order to 
process a stock webpage and retrieve stock indices for data analysis.

'''

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from datetime import datetime
import csv

def get_html(url):
    '''
        Accepts a single URL argument and makes an HTTP GET request to that URL. If nothing goes wrong and
        the content-type of the response is some kind of HTML/XML, return the raw HTML content for the 
        requested page. However, if there were problems with the request, return None.
    '''
    header = {
                 "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                 "X-Requested-With": "XMLHttpRequest"
             }
    try:
        with closing(get(url, stream=True, headers=header)) as resp:
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

def get_stocks(stocks):
    '''
        Accepts a list of stock webpages as an arguments. Then downloads the webpages, finds <h1> and <span> 
        elements, and puts the stock names, prices, net change and percentage change into a list to be returned.
    '''
    data = []
    for st in stocks:
        response = get_html(st)

        if response is not None:
            soup = BeautifulSoup(response, "html.parser")

            name = soup.find("h1", {"class": "companyName__99a4824b"}).text.strip()
            price = soup.find("span", {"class": "priceText__1853e8a5"}).text
            net_change = soup.find("span", {"class": "changeAbsolute__395487f7"}).text
            perc_change = soup.find("span", {"class": "changePercent__2d7dc0d2"}).text
	
            data.append((name, price, net_change, perc_change))
        else:
            raise Exception(f"There was an error retrieving contents at {st}")
    return data

def write_stocks(region, data):
    ''' 
        Accepts a region and item list as an argument, proceses through the list and writes all the stock info
        into a single CSV data file.
    '''
    filename = f"{region}_stocks.csv"

    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "price", "net_change", "perc_change", "datetime"])
        for name, price, net_change, perc_change in data:
            writer.writerow([name, price, net_change, perc_change, datetime.now()])

if __name__ == "__main__":
    '''

        1. Initalize the list of URLs for American, European and Asian stocks.
        2. Get list of all stock information.
        3. Write all the stock information to individual CSV data files.

    '''
    americas_st = [ 
                      "https://www.bloomberg.com/quote/INDU:IND",
                      "https://www.bloomberg.com/quote/SPX:IND",
                      "https://www.bloomberg.com/quote/CCMP:IND",
                      "https://www.bloomberg.com/quote/NYA:IND",
                      "https://www.bloomberg.com/quote/SPTSX:IND"
                  ]

    europe_st = [
                    "https://www.bloomberg.com/quote/SX5E:IND",
                    "https://www.bloomberg.com/quote/UKX:IND",
                    "https://www.bloomberg.com/quote/DAX:IND",
                    "https://www.bloomberg.com/quote/CAC:IND",
                    "https://www.bloomberg.com/quote/IBEX:IND"
                ]

    asia_st = [
                  "https://www.bloomberg.com/quote/NKY:IND",
                  "https://www.bloomberg.com/quote/TPX:IND",
                  "https://www.bloomberg.com/quote/HSI:IND",
                  "https://www.bloomberg.com/quote/SHSZ300:IND",
                  "https://www.bloomberg.com/quote/AS51:IND"
              ]

    print("Getting list of American stock information...")
    americas_data = get_stocks(americas_st)
    print(".../done")

    print("Getting list of European stock information...")
    europe_data = get_stocks(europe_st)
    print(".../done")

    print("Getting list of Asian stock information...")          
    asian_data = get_stocks(asia_st)
    print(".../done")


    print("Writing American stock information to a CSV file...")
    write_stocks("american", americas_data)
    print(".../done")

    print("Writing European stock information to a CSV file...")
    write_stocks("european", europe_data)
    print(".../done")    

    print("Writing Asian stock information to a CSV file...")
    write_stocks("asian", asian_data)
    print(".../done")