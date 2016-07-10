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


def clean_string(to_clean):
    if not to_clean:
        return None
    result = to_clean.strip()
    result = re.sub('\n', ' ', result)
    result = re.sub(' +', ' ', result)
    return result


def check_is_city(val):
    result = False
    for i in range(0, len(cities_regex)):
        regex = cities_regex[i]
        is_match = cities[i] if re.match(regex, val) else False
        result = result or is_match
    return result


def check_city_recursive(to_check):
    result = check_is_city(str(to_check.encode('utf8')))

    if not result:
        if hasattr(to_check, 'contents'):
            for content in to_check.contents:
                result = result or check_city_recursive(content)

    return result


f = codecs.open('FINAL_DESTINATIONS_simple.html', 'r', 'utf-8')

html_source = f.read()
soup = BeautifulSoup(html_source, 'html.parser')
target_elements = ["p", "h1", "h2", "h3", "h4", "strong"]
heading_elements = ["h1", "h2", "h3", "h4", "strong"]

result_dict = {}
current_destination = []
current_destination_name = None
current_city = {}
current_city_name = None

elements = soup.findAll(target_elements)

for element in elements:

    if element.name == "p":  # If element is a block of text
        # add to current destination
        # print element.string
        if element.string:
            current_destination.append(clean_string(element.string))

    else:  # element is either a destination or city

        city_name = check_city_recursive(element)
        if city_name:  # element is a city
            # New City found
            print "Found city: " + city_name
            if not current_city_name == city_name:  # Write out contents of current city, and create new city
                result_dict[current_city_name] = current_city
                current_city_name = city_name
                current_city = {}

        else:  # element is a destination
            current_city[current_destination_name] = current_destination
            current_destination_name = clean_string(element.string)
            current_destination = []

# Write results to file
path = os.path.join(os.getcwd(), "output")

if not os.path.exists(path):
    os.makedirs(path)

with open(os.path.join(path, 'final_destinations.json'), 'w') as fp:
    json.dump(result_dict, fp)

print("\nFinished")
print("Check \'output\' folder for data")
