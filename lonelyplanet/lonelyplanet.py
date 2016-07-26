import codecs
import io
import json
import os
import re
import urllib
from bs4 import BeautifulSoup

print "Processing file..."

f = codecs.open(
    'Sights in Rajasthan, India - Lonely Planet.html',
    'r', 'utf-8')

html_source = f.read()
soup = BeautifulSoup(html_source, 'html.parser')

times_dict = {}
times_dict_all = {}

places = soup.findAll("div", {
    "class": "col--one-whole nv--col--one-half mv--col--one-third lv--col--one-quarter wv--col--one-third cv--col--one-quarter"})

print len(places)
for place in places:
    # print place
    # name = place.contents[1].contents[1].contents[1].contents[1].contents
    name = place.findAll("h1", {"class": "card__content__title js-prerender-title"})[0].string
    link = place.findAll("a")[0].get("href")
    print name

    uopen = urllib.urlopen(link)
    print "Opened " + link
    html_source = uopen.read()
    soup = BeautifulSoup(html_source, 'html.parser')
    print soup

    table = soup.findAll(['dd', 'dt'])
    print table

    # times = "Unknown"
    # if len(poi_text) > 0:
    #     times = poi_text[0].contents[1].string
    #     times_dict[name] = times
    # times_dict_all[name] = times

# Write results to file
path = os.path.join(os.getcwd(), "output")

if not os.path.exists(path):
    os.makedirs(path)

with open(os.path.join(path, 'lonely_planet_times.json'), 'w') as fp:
    json.dump(times_dict, fp, False, True, True, True, None, 2, None, 'utf-8', None, True)

with open(os.path.join(path, 'lonely_planet_times_all.json'), 'w') as fp:
    json.dump(times_dict_all, fp, False, True, True, True, None, 2, None, 'utf-8', None, True)

print("\nFinished")
print("Check \'output\' folder for data")
