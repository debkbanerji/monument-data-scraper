import urllib
from bs4 import BeautifulSoup

url = "http://www.monumentsofdelhi.com/monuments"
uopen = urllib.urlopen(url)
html_source = uopen.read()

soup = BeautifulSoup(html_source, 'html.parser')

monument_panels = soup.findAll("div", {"class": "panel-body"})

print monument_panels.__len__()

monument_links = []
for panel in monument_panels:
    monument_links.append("http://www.monumentsofdelhi.com/" + str(panel.contents[9].contents[1].get('href')))
    # for child in panel.contents:
    #     # link = panel.descendants
    #     # print link

monuments = []

# for link in monument_links:

link = monument_links[0]
uopen = urllib.urlopen(link)
html_source = uopen.read()

soup = BeautifulSoup(html_source, 'html.parser')
monument_name = soup.h1.contents[1].string
print "\n"
print monument_name
panel = soup.findAll("div", {"class": "panel-warning"})
# print panel[0]
keys = panel[0].findAll("th", {"class": "col-xs-4"})
values = panel[0].findAll("td", {"class": "col-xs-8"})
# print keys
# print len(keys)
# print values
# print len(values)
for i in range(0,10):
    print ("\"" + str((keys[i].contents[0] or [""])) + "\": \"" + str(values[i].contents[0]) + "\",")