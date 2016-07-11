import json
import os
import urllib
from bs4 import BeautifulSoup

path = os.path.join(os.getcwd(), "output")

if not os.path.exists(path):
    os.makedirs(path)

exhibit_links = ["/culturalinstitute/beta/exhibit/QRUxWeZM", "/culturalinstitute/beta/exhibit/QRUfDAo-",
                 "/culturalinstitute/beta/exhibit/QRVw3eVt", "/culturalinstitute/beta/exhibit/QRXJIPZO",
                 "/culturalinstitute/beta/exhibit/QRUUiMQd", "/culturalinstitute/beta/exhibit/QRWtlyd7",
                 "/culturalinstitute/beta/exhibit/QRWvANZ3", "/culturalinstitute/beta/exhibit/QRU8El0t"]
# exhibit_links = ["/culturalinstitute/beta/exhibit/QRUxWeZM"]

# for each page
for link in exhibit_links:
    url = "https://www.google.com/culturalinstitute/beta/u/0/search/exhibit?p=indian-national-trust-for-art-and-cultural-heritage"
    uopen = urllib.urlopen("https://www.google.com" + link)
    html_source = uopen.read()
    soup = BeautifulSoup(html_source, 'html.parser')
    divs = soup.findAll("div", {"class": "PECUof"})
    print divs

print("\nFinished")
print("Check \'output\' folder for data")
