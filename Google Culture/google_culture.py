import codecs
import json
import os
import re
import requests
import urllib
from bs4 import BeautifulSoup


def extract_raw_image(target_url, directory_name, file_name=None):
    output_path = os.path.join(os.getcwd(), "output", directory_name)

    if not file_name:
        url_split = target_url.split("/")
        file_name = url_split[len(url_split) - 1]

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_path = os.path.join(output_path, file_name)
    output_count = 0

    while os.path.isfile(output_path + "-" + str(output_count) + ".jpeg"):
        output_count += 1

    f = open(output_path + "-" + str(output_count) + ".jpeg", "ab")
    f.write(requests.get(target_url).content)
    f.close()


def extract_image(page_url, directory_name):
    uopen = urllib.urlopen(page_url)
    html_source = uopen.read()
    html_source = html_source.decode('ascii', 'ignore')

    soup = BeautifulSoup(html_source, 'html.parser')
    heading = soup.findAll("h1", {"class": "EReoAc"})

    image_name = heading[0].string

    search_obj = re.search(r'"http(.*)ggpht.com(.*)"', html_source)
    components = str(search_obj.group()).split("\"")
    image_url = components[1]
    extract_raw_image(image_url, directory_name, image_name)


def recursive_div_scan(div):
    if hasattr(div, "name") and div.name == "a":
        image_links.append(div.get("href"))
        return div.get("href")
    if hasattr(div, "contents"):
        result = []
        for element in div.contents:
            result.append(recursive_div_scan(element))
    else:
        result = str(div)
    return result


path = os.path.join(os.getcwd(), "output")

if not os.path.exists(path):
    os.makedirs(path)

exhibit_links = ["/culturalinstitute/beta/exhibit/QRUxWeZM", "/culturalinstitute/beta/exhibit/QRUfDAo-",
                 "/culturalinstitute/beta/exhibit/QRVw3eVt", "/culturalinstitute/beta/exhibit/QRXJIPZO",
                 "/culturalinstitute/beta/exhibit/QRUUiMQd", "/culturalinstitute/beta/exhibit/QRWtlyd7",
                 "/culturalinstitute/beta/exhibit/QRWvANZ3", "/culturalinstitute/beta/exhibit/QRU8El0t"]
exhibit_names = ["Lodi Garden Monuments", "Qutb Complex", "Central Vista", "Hauz Khas Complex", "Baolis of Delhi",
                 "Firoz Shah Kotla", "Purana Qila", "Red Fort"]
# exhibit_links = ["/culturalinstitute/beta/exhibit/QRUxWeZM"]


# for each page
for i in range(0, len(exhibit_links)):
    link = exhibit_links[i]
    uopen = urllib.urlopen("https://www.google.com" + link)
    html_source = uopen.read()
    html_source = html_source.decode('ascii', 'ignore')
    soup = BeautifulSoup(html_source, 'html.parser')
    divs = soup.findAll("div", {"class": "PECUof"})

    image_links = []
    div_array = []
    for div in divs:
        div_array.append(recursive_div_scan(div))

    for link in image_links:
        # Extract image from page
        link = "https://www.google.com" + link
        folder_name = os.path.join(exhibit_names[i], link.split("/")[6])

        print "Extracting image from " + link + " to " + folder_name
        try:
            extract_image(link, folder_name)
        except Exception:
            print "Error extracting: page may not be in expected format"

    with open(os.path.join(path, 'results.json'), 'w') as fp:
        json.dump(div_array, fp, False, True, True, True, None, 2, None, 'utf-8', None, True)

print("\nFinished")
print("Check \'output\' folder for data")
