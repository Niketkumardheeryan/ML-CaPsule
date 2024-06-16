# Web-Scraping

Web scraping is the process of collecting structured web data in an automated fashion.
In general, web scraping is essentially to extract vast amount of publicly available web data to make smarter decisions.

A collection of small programs that extract data from a websites with the use of BeautifulSoup, a Python package for parsing HTML and XML documents. Once you retrive the raw HTML of a site, you can start to select and extract with BeautifulSoup, which parses raw HTML strings and produces an object that mirrors HTML documents' structure.

## Requirements

To run this script, you need to have Python installed on your system. Additionally, you need to install the following Python packages:

- `requests`: For making HTTP requests to fetch web pages.
- `beautifulsoup4`: For parsing and extracting data from HTML.

## Installation

You can install the required packages using `pip`. Open your terminal or command prompt and run the following commands:

```sh
pip install requests
pip install beautifulsoup4
```

### The Rules of Scraping
1. Check a website's Term and Conditions before scraping it and read the statements about legal use of the data. 
2. Do not request data from the website too aggressiely and ensure that your program behaves in a reasonable manner.
3. Revisit the website and rewrite code as needed as the layout of the site may change.