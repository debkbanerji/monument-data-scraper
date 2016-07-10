import codecs
import io
import json
import os
import re
# import urllib
from bs4 import BeautifulSoup

cities = ["Jaipur", "Jodhpur", "Ajmer", "Udaipur", "Kota", "Bharatpur", 'Chittorgarh',
          "Alwar", "Bikaner", "Bundi", "Banswara", "Churu", "Dungarpur",
          "Ganganagar", "Hanumangarh", "Jaisalmer", "Mount Abu",
          "Ranthambhore", "Shekhawati", "Other Places"]

cities_regex = [r'([ ,\n]*)Jaipur([ ,\n]*)$', r'([ ,\n]*)Jodhpur([ ,\n]*)$', r'([ ,\n]*)Ajmer([ ,\n]*)$',
                r'([ ,\n]*)Udaipur([ ,\n]*)$', r'([ ,\n]*)Kota([ ,\n]*)$',
                r'([ ,\n]*)Bharatpur([ ,\n]*)$', r'([ ,\n]*)Chittorgarh([ ,\n]*)$',
                r'([ ,\n]*)Alwar([ ,\n]*)$', r'([ ,\n]*)Bikaner([ ,\n]*)$', r'([ ,\n]*)Bundi([ ,\n]*)$',
                r'([ ,\n]*)Banswara([ ,\n]*)$', r'([ ,\n]*)Churu([ ,\n]*)$',
                r'([ ,\n]*)Dungarpur([ ,\n]*)$',
                r'([ ,\n]*)Ganganagar([ ,\n]*)$', r'([ ,\n]*)Hanumangarh([ ,\n]*)$', r'([ ,\n]*)Jaisalmer([ ,\n]*)$',
                r'([ ,\n]*)Mount Abu([ ,\n]*)$',
                r'([ ,\n]*)Ranthambhore([ ,\n]*)$', r'([ ,\n]*)Shekhawati([ ,\n]*)$',
                r'([ ,\n]*)Other Places([ ,\n]*)$']


def check_city(val):
    result = False
    for regex in cities_regex:
        if re.match(regex, val):
            print "Found city: " + val
        is_match = True if re.match(regex, val) else False
        result = result or is_match
        # print result
    return result


def check_city_recursive(to_check):
    result = check_city(str(to_check.encode('utf8')))

    if not result:
        # check if nested element is a city

        # check if nested elements exist
        if hasattr(to_check, 'contents'):
            for content in to_check.contents:
                result = result or check_city_recursive(content)

    return result


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


f = codecs.open('FINAL_DESTINATIONS_simple.html', 'r', 'utf-8')

html_source = f.read()
# print(html_source)

soup = BeautifulSoup(html_source, 'html.parser')
# print re.match(cities_regex[0], "\nJaipur")

heading_elements = ["strong", "h1", "h2", "h3", "h4"]

result_array = {}

# print current_section.name

elements = soup.findAll(["p", "h1", "h2", "h3", "h4", "strong"])

# print elements

for element in elements:
    # print element
    if check_city_recursive(element):
        # pass
        print "MATCH: " + str(element)

path = os.path.join(os.getcwd(), "output")

if not os.path.exists(path):
    os.makedirs(path)

print("\nFinished")
print("Check \'output\' folder for data")
