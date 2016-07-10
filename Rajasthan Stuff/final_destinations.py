import codecs
import io
import json
import os
import re
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


def get_string_recursive(target_element):
    result = None
    if target_element:
        if target_element.string:
            result = clean_string(target_element.string)
        elif target_element.contents:
            content_string = ""
            for content_item in target_element.contents:
                content_string = content_string + (get_string_recursive(content_item) or "")
            result = content_string
    return result


print "Processing file..."

f = codecs.open('FINAL_DESTINATIONS_simple.html', 'r', 'utf-8')

html_source = f.read()
soup = BeautifulSoup(html_source, 'html.parser')
target_elements = ["p", "h1", "h2", "h3", "h4", "strong"]
heading_elements = ["h1", "h2", "h3", "h4", "strong"]

result_dict = {}
current_subheading = []
current_subheading_name = None
current_city = {}
current_city_name = None

elements = soup.findAll(target_elements)

for element in elements:

    if element.name == "p":  # If element is a block of text
        # add to current destination
        if element.string:
            current_subheading.append(get_string_recursive(element.string))

    else:  # element is either a destination or city

        city_name = check_city_recursive(element)
        if city_name:  # element is a city
            # New City found
            if not current_city_name == city_name:  # Write out contents of current city, and create new city
                result_dict[current_city_name] = current_city
                current_city_name = city_name
                current_city = {}

        else:  # element is a destination
            current_city[current_subheading_name] = current_subheading
            # current_destination_name = clean_string(element.string)
            current_subheading_name = get_string_recursive(element)
            current_subheading = []

# Write results to file
path = os.path.join(os.getcwd(), "output")

if not os.path.exists(path):
    os.makedirs(path)

with open(os.path.join(path, 'final_destinations.json'), 'w') as fp:
    json.dump(result_dict, fp)

with open(os.path.join(path, 'final_destinations.pretty.json'), 'w') as fp:
    json.dump(result_dict, fp, False, True, True, True, None, 2, None, 'utf-8', None, True)


print("\nFinished")
print("Check \'output\' folder for data")
