import json
import os
# import urllib
from bs4 import BeautifulSoup

class section:
    def __init__(self):
        self.name = "Heading"
        self.paragraphs = []

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


f = open('FINAL_DESTINATIONS.html', 'r')

html_source = f.read()
# print(html_source)

soup = BeautifulSoup(html_source, 'html.parser')

heading_elements = ["p"]

sections = []
current_section = section()
# print current_section.name

elements = soup.findAll(["p", "strong", "h1", "h2", "h3", "h4"])

# print elements

for element in elements:
    print element.name
    if element.name in heading_elements:
        print element.decode_contents(formatter="html")

#
# monument_panels = soup.findAll("div", {"class": "panel-body"})
#
# print("Scraping data for " + str(monument_panels.__len__()) + " monuments...\n")
#
# monument_links = []
# for panel in monument_panels:
#     monument_links.append("http://www.monumentsofdelhi.com/" + str(panel.contents[9].contents[1].get('href')))
#
# output_array = []
# output_map = {}
#
# for link in monument_links:
#
#     uopen = urllib.urlopen(link)
#     html_source = uopen.read()
#
#     soup = BeautifulSoup(html_source, 'html.parser')
#     # monument_name = soup.h1.contents[1].string
#
#     panel = soup.findAll("div", {"class": "panel-warning"})
#     keys = panel[0].findAll("th", {"class": "col-xs-4"})
#     values = panel[0].findAll("td", {"class": "col-xs-8"})
#
#     monument_dict = {}
#     for i in range(0, len(keys)):
#         if len(values[i].contents) > 0:
#             value = str(values[i].contents[0])
#         else:
#             value = ""
#         if len(keys[i].contents[0].contents) > 0:
#             monument_dict[str(keys[i].contents[0].contents[0])] = value
#         else:
#             monument_dict[str(keys[i - 1].contents[0].contents[0])] = monument_dict[str(
#                 keys[i - 1].contents[0].contents[0])] + "\n" + value
#
#     if 'Coordinates' in monument_dict:
#         coordinates = monument_dict['Coordinates'].split(', ')
#         monument_dict['Latitude'] = coordinates[0]
#         monument_dict['Longitude'] = coordinates[1]
#         del monument_dict['Coordinates']
#
#     monument_name = monument_dict['Name']
#     excerpt_span = soup.findAll("span", {"id": "cpContent_lblExcerpt"})
#
#     if len(excerpt_span[0].contents) > 0:
#         description = excerpt_span[0].contents[0]
#         monument_dict['Description'] = description
#
#     # Removing name from monument_dict and saving to output_map
#     monument_dict_for_map = removekey(monument_dict, 'Name')
#     output_map[monument_name] = monument_dict_for_map
#
#     output_array.append(monument_dict)
#     print(monument_dict['Name'])
#
#

path = os.path.join(os.getcwd(), "output")

if not os.path.exists(path):
    os.makedirs(path)

print("\nFinished")
print("Check \'output\' folder for data")
