import codecs
import io
import json
import os
import re
import urllib
from bs4 import BeautifulSoup

places_array_master = []
places_dict_master = {}


# f = codecs.open(
#     '361 Places to Visit in Jaipur, Tourist Places in Jaipur, Sightseeing and Attractions _ ixigo Travel Guide.html',
#     'r', 'utf-8')

def extract_data(name, file_name):
    print "Extracting data for: " + name + " from file " + file_name
    f = codecs.open(
        file_name,
        'r', 'utf-8')
    html_source = f.read()
    soup = BeautifulSoup(html_source, 'html.parser')
    places_dict = {}
    places_array = []
    places = soup.findAll("div", {"class": "namedentity-item row"})
    for place in places:

        place_dict = {}

        place_name = place.contents[3].contents[3].contents[1].string
        poi_text = place.findAll("div", {"class": "poi-text"})
        link = place.findAll("a")[1].get("href")
        print "\n" + place_name
        print link
        # times = "Unknown"
        # if len(poi_text) > 0:
        #     times = poi_text[0].contents[1].string
        #
        # place_dict["times"] = times

        url = link
        uopen = urllib.urlopen(url)
        place_html_source = uopen.read()

        place_soup = BeautifulSoup(place_html_source, 'html.parser')
        # print html_source

        # Building place_dict:

        timing_container = place_soup.findAll("div", {"class": "timing-container"})
        if len(timing_container) > 0:
            timing_containter = timing_container[0]
            days_of_week = timing_containter.findAll("div", {"class": "day-of-week"})
            if len(days_of_week) > 0:
                place_dict["days-of-week"] = days_of_week[0].string
            working_hour = timing_containter.findAll("div", {"class": "working-hour"})
            if len(working_hour) > 0:
                place_dict["timings"] = working_hour[0].string

        pricing_container = place_soup.findAll("div", {"id": "entryfee"})
        if len(pricing_container) > 0:
            pricing_container = pricing_container[0]
            price_list = pricing_container.findAll("div", {"class": "list-wrapper-box"})
            price_list = price_list[0].findAll("div", {"class": "list-item"})
            prices = {}
            for price in price_list:
                print "PRICE: " + str(price)
                price_vals = price.findAll("span", {"class": "bold"})
                if len(price_vals) > 0:
                    price_val = price_vals[0].string.rstrip().lstrip()
                    price_keys = price.findAll("span", {"class": ""})
                    if len(price_keys) < 1:
                        # print "REFINDING PRICE KEYS"
                        price_keys = price.findAll("span", {"class": "i-b price-unit"})
                    price_key = price_keys[0].string.lstrip().rstrip()
                    if len(price_keys) > 1 and price_keys[1].string:
                        price_key = price_key + " " + price_keys[1].string.lstrip().rstrip()
                    # print price_key + ": " + price_val
                    prices[price_key] = price_val
            # print prices
            place_dict["prices"] = prices

        print place_dict
        places_dict[place_name] = place_dict
        places_dict_master[place_name] = place_dict

        place_dict["name"] = place_name
        places_array.append(place_dict)
        places_array_master.append(place_dict)

    # Write results to file
    path = os.path.join(os.getcwd(), "output", "maps")
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, 'ixigo_data_' + name + '.json'), 'w') as fp:
        json.dump(places_dict, fp, False, True, True, True, None, 2, None, 'utf-8', None, True)

    # Write results to file
    path = os.path.join(os.getcwd(), "output", "arrays")
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, 'ixigo_data_' + name + '.json'), 'w') as fp:
        json.dump(places_array, fp, False, True, True, True, None, 2, None, 'utf-8', None, True)


files = {
    "Ajmer":
        "Ajmer.html",
    "Alwar":
        "Alwar.html",
    "Banswara":
        "Banswara.html",
    "Bharatpur":
        "Bharatpur.html",
    "Bikaner":
        "Bikaner.html",
    "Bundi":
        "Bundi.html",
    "Chittorgarh":
        "Chittorgarh.html",
    "Churu":
        "Churu.html",
    "Dungarpur":
        "Dungarpur.html",
    "Ganganagar":
        "Ganganagar.html",
    "Hanumangarh":
        "Hanumangarh.html",
    "Jaipur":
        "Jaipur.html",
    "Jaisalmer":
        "Jaisalmer.html",
    "Jodhpur":
        "Jodhpur.html",
    "Kota":
        "Kota.html",
    "Mount Abu":
        "Mount Abu.html",
    "Ranthambore":
        "Ranthambore.html",
    "Udaipur":
        "Udaipur.html"

}

for f in files.keys():
    extract_data(f, files[f])

with open(os.path.join(os.getcwd(), "output", 'ixigo_data_array.json'), 'w') as fp:
    json.dump(places_array_master, fp, False, True, True, True, None, 2, None, 'utf-8', None, True)
with open(os.path.join(os.getcwd(), "output", 'ixigo_data_map.json'), 'w') as fp:
    json.dump(places_dict_master, fp, False, True, True, True, None, 2, None, 'utf-8', None, True)

print("\nFinished")
