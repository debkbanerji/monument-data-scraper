import json
import urllib
from bs4 import BeautifulSoup

url = "http://www.monumentsofdelhi.com/monuments"
uopen = urllib.urlopen(url)
html_source = uopen.read()

soup = BeautifulSoup(html_source, 'html.parser')

monument_panels = soup.findAll("div", {"class": "panel-body"})

print "Scraping data for " + str(monument_panels.__len__()) + " monuments...\n"

monument_links = []
for panel in monument_panels:
    monument_links.append("http://www.monumentsofdelhi.com/" + str(panel.contents[9].contents[1].get('href')))
    # for child in panel.contents:
    #     # link = panel.descendants
    #     # print link

monuments = []

for link in monument_links:

    uopen = urllib.urlopen(link)
    html_source = uopen.read()

    soup = BeautifulSoup(html_source, 'html.parser')
    monument_name = soup.h1.contents[1].string

    panel = soup.findAll("div", {"class": "panel-warning"})
    # print panel[0]
    keys = panel[0].findAll("th", {"class": "col-xs-4"})
    values = panel[0].findAll("td", {"class": "col-xs-8"})
    # print keys
    # print len(keys)
    # print values
    # print len(values)
    monument_dict = {}
    # print "\n"
    for i in range(0, len(keys)):
        if len(values[i].contents) > 0:
            value = str(values[i].contents[0])
        else:
            value = ""
        # print ("\"" + str((keys[i].contents[0] or [""])) + "\": \""
        #        + value + "\",")
        if len(keys[i].contents[0].contents) > 0:
            # print keys[i].contents[0].contents[0]
            monument_dict[str(keys[i].contents[0].contents[0])] = value
        else:
            monument_dict[str(keys[i - 1].contents[0].contents[0])] = monument_dict[str(
                keys[i - 1].contents[0].contents[0])] + "\n" + value

    if 'Coordinates' in monument_dict:
        coordinates = monument_dict['Coordinates'].split(', ')
        monument_dict['Latitude'] = coordinates[0]
        monument_dict['Longitude'] = coordinates[1]
        del monument_dict['Coordinates']

    monuments.append(monument_dict)
    print "Finished scraping " + monument_dict['Name']

with open('monumentsofdelhi.json', 'w') as fp:
    json.dump(monuments, fp)

print "\nFinished"
print "Check file \'monumentsofdelhi.json\' for data"
