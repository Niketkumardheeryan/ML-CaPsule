from bs4 import BeautifulSoup
import requests
import pandas

req = requests.get("http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
soup = BeautifulSoup(req.content, "html.parser")
pageNum = soup.find_all("a", {"class", "Page"})[-1].text

baseURL = "http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
infoSet = []

for page in range(0, int(pageNum)*10, 10):
    req = requests.get(baseURL + str(page) + ".html")
    soup = BeautifulSoup(req.content, "html.parser")
    dataSet = soup.find_all("div", {"class": "propertyRow"})

    for data in dataSet:
        d = {}
        try:
            d["Price"] = data.find("h4", {"class": "propPrice"}).text.strip()
        except:
            d["Price"] = None

        try:
            d["Address"] = data.find_all("span", {"class": "propAddressCollapse"})[0].text
        except:
            d["Address"] = None
        
        try:
            d["Locality"] = data.find_all("span", {"class": "propAddressCollapse"})[1].text
        except:
            d["Locality"] = None

        try:
            d["Beds"] = data.find("span", {"class", "infoBed"}).find("b").text
        except:
            d["Beds"] = None

        try:
            d["Area"] = data.find("span", {"class", "infoSqFt"}).find("b").text
        except:
            d["Area"] = None

        try:
            d["Full Bath"] = data.find("span", {"class", "infoValueFullBath"}).find("b").text
        except:
            d["Full Bath"] = None

        try:
            d["Half Bath"] = data.find("span", {"class", "infoValueHalfBath"}).find("b").text
        except:
            d["Half Bath"] = None

        for columnGroup in data.find_all("div", {"class": "columnGroup"}):
            for featureGroup, featureName in zip(columnGroup.find_all("span", {"class", "featureGroup"}), columnGroup.find_all("span", {"class:", "featureName"})):
                if "Lot Size" in featureGroup.text:
                    d["Lot Size"] = featureName.text
                else:
                    d["Lot Size"] = None
        infoSet.append(d)

df = pandas.DataFrame(infoSet)
df.to_csv("propertyInfo.csv")