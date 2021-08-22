# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 00:16:12 2021

@author: ellix
"""

import json
import menu_scraper
import restaurant_scraper


base_url = "https://www.ubereats.com/ca/category/"
result = []

""" ===== Restaurant Menu Scraper ===== """

    #restaurant_scraper.scrape_restaurants(base_url, city)

file = open('restaurant_urls.txt', 'r')
lines = file.readlines()

for line in lines:
    try:  
        result.append(menu_scraper.scrape_menu(line))
    except Exception as ex: 
        print ("didn't work ", ex)
        continue
        

with open('data.json', 'w+', encoding='utf-8') as outfile:
    json.dump(result, outfile, indent=4, ensure_ascii=False)