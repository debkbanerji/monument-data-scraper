import json
import os
import urllib
from bs4 import BeautifulSoup


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


url = "http://www.monumentsofdelhi.com/monuments"
uopen = urllib.urlopen(url)
html_source = uopen.read()

soup = BeautifulSoup(html_source, 'html.parser')

monument_panels = soup.findAll("div", {"class": "panel-body"})

print("Scraping data for " + str(monument_panels.__len__()) + " monuments...\n")

monument_links = []
for panel in monument_panels:
    monument_links.append("http://www.monumentsofdelhi.com/" + str(panel.contents[9].contents[1].get('href')))

output_array = []
output_map = {}

for link in monument_links:

    uopen = urllib.urlopen(link)
    html_source = uopen.read()

    soup = BeautifulSoup(html_source, 'html.parser')
    # monument_name = soup.h1.contents[1].string

    panel = soup.findAll("div", {"class": "panel-warning"})
    keys = panel[0].findAll("th", {"class": "col-xs-4"})
    values = panel[0].findAll("td", {"class": "col-xs-8"})

    monument_dict = {}
    for i in range(0, len(keys)):
        if len(values[i].contents) > 0:
            value = str(values[i].contents[0])
        else:
            value = ""
        if len(keys[i].contents[0].contents) > 0:
            monument_dict[str(keys[i].contents[0].contents[0])] = value
        else:
            monument_dict[str(keys[i - 1].contents[0].contents[0])] = monument_dict[str(
                keys[i - 1].contents[0].contents[0])] + "\n" + value

    if 'Coordinates' in monument_dict:
        coordinates = monument_dict['Coordinates'].split(', ')
        monument_dict['Latitude'] = coordinates[0]
        monument_dict['Longitude'] = coordinates[1]
        del monument_dict['Coordinates']

    monument_name = monument_dict['Name']
    excerpt_span = soup.findAll("span", {"id": "cpContent_lblExcerpt"})

    if len(excerpt_span[0].contents) > 0:
        description = excerpt_span[0].contents[0]
        monument_dict['Description'] = description

    # Removing name from monument_dict and saving to output_map
    monument_dict_for_map = removekey(monument_dict, 'Name')
    output_map[monument_name] = monument_dict_for_map

    output_array.append(monument_dict)
    print(monument_dict['Name'])

path = os.path.join(os.getcwd(), "output")

if not os.path.exists(path):
    os.makedirs(path)

with open(os.path.join(path, 'monumentsofdelhi.array.json'), 'w') as fp:
    json.dump(output_array, fp)

with open(os.path.join(path, 'monumentsofdelhi.map.json'), 'w') as fp:
    json.dump(output_map, fp)

with open(os.path.join(path, 'monumentsofdelhi.array.pretty.json'), 'w') as fp:
    json.dump(output_array, fp, False, True, True, True, None, 2, None, 'utf-8', None, True)

with open(os.path.join(path, 'monumentsofdelhi.map.pretty.json'), 'w') as fp:
    json.dump(output_map, fp, False, True, True, True, None, 2, None, 'utf-8', None, True)

print("\nFinished")
print("Check \'output\' folder for data")
