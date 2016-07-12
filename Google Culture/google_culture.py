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
    uopen_image = urllib.urlopen(page_url)
    html_source_image = uopen_image.read()
    html_source_image = html_source_image.decode('ascii', 'ignore')

    soup = BeautifulSoup(html_source_image, 'html.parser')
    heading = soup.findAll("h1", {"class": "EReoAc"})

    image_name = heading[0].string

    search_obj = re.search(r'"http(.*)ggpht.com(.*)"', html_source_image)
    components = str(search_obj.group()).split("\"")
    image_url = components[1]
    extract_raw_image(image_url, directory_name, image_name)


def recursive_div_scan(target_div):
    if hasattr(target_div, "name") and target_div.name == "a":
        image_links.append(target_div.get("href"))
        return target_div.get("href")
    if hasattr(target_div, "contents"):
        if len(target_div.contents) > 1:
            result = []
            for element in target_div.contents:
                to_append = recursive_div_scan(element)
                if to_append:
                    result.append(to_append)
        elif len(target_div.contents) == 1:
            result = recursive_div_scan(target_div.contents[0])
        else:
            result = None
    else:
        result = str(target_div)

        exhibit_result_array.append(result)
        global_result_array.append(result)
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

global_result_array = []
global_result_map = {}


# for each page
for i in range(0, len(exhibit_links)):
    global_result_array.append("EXHIBIT: " + exhibit_names[i])
    exhibit_result_array = []

    link = exhibit_links[i]
    uopen = urllib.urlopen("https://www.google.com" + link)
    html_source = uopen.read()
    html_source = html_source.decode('ascii', 'ignore')
    soup = BeautifulSoup(html_source, 'html.parser')
    divs = soup.findAll("div", {"class": "PECUof"})

    if not os.path.exists(os.path.join(path, exhibit_names[i])):
        os.makedirs(os.path.join(path, exhibit_names[i]))

    exhibit_text = []

    image_links = []
    for div in divs:
        exhibit_text.append(recursive_div_scan(div))

    # Image extraction
    # for link in image_links:
    #     # Extract image from page
    #     link = "https://www.google.com" + link
    #     folder_name = os.path.join(exhibit_names[i], link.split("/")[6])
    #
    #     print "Extracting image from " + link + " to " + folder_name
    #     try:
    #         extract_image(link, folder_name)
    #     except Exception:
    #         print "Error extracting: page may not be in expected format"

    global_result_map[exhibit_names[i]] = exhibit_result_array

    with open(os.path.join(path, exhibit_names[i], 'results.json'), 'w') as fp:
        json.dump(exhibit_text, fp, False, True, True, True, None, 2, None, 'utf-8', None, True)


with open(os.path.join(path, 'results.array.json'), 'w') as fp:
    json.dump(global_result_array, fp, False, True, True, True, None, 2, None, 'utf-8', None, True)

with open(os.path.join(path, 'results.map.json'), 'w') as fp:
    json.dump(global_result_map, fp, False, True, True, True, None, 2, None, 'utf-8', None, True)


print("\nFinished")
print("Check \'output\' folder for data")
