# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 00:16:12 2021

@author: ellix
"""

import json
import menu_scraper
import restaurant_scraper


base_url = "https://www.ubereats.com/ca/category/"
city_list = ["oakville-on"]
restaurant_data = {
    'cities': []
}
temp_array = []

""" ===== Restaurant Menu Scraper ===== """
for city in city_list:

    #restaurant_scraper.scrape_restaurants(base_url, city)

    file = open(city + '_restaurant_urls.txt', 'r')
    lines = file.readlines()

    for line in lines:
        try:  
            temp_array.append(menu_scraper.scrape_menu(line))
        except Exception as ex: 
            print ("didn't work ", ex)
            continue

    restaurant_data['cities'].append({
        city: temp_array
    })

with open('data.json', 'w+', encoding='utf-8') as outfile:
    json.dump(restaurant_data, outfile, indent=4, ensure_ascii=False)