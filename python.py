# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 23:53:35 2021

@author: ellix
"""

from selenium import webdriver
import populartimes
import json
import menu_scraper
import restaurant_scraper
import os
from flask import Flask, jsonify, request, render_template
import datetime

app = Flask(__name__)
restaurants = []
food = None

class Restaurant(): 
    def __init__(self, name, address):
        self.name = name
        self.address = address 
        self.distance = 0 
        self.menu = ''
        self.lat = 0 
        self.lng = 0 
        self.rating = 0 
        self.priceLvl = 0 
        
    def printSelf(self):
        print ('name, ', self.name)
        print ('address, ', self.address)
        print ('lat, ', self.lat)
        print ('lng, ', self.lng)
        print ('rating, ', self.rating)
        print ('pricelvl, ', self.priceLvl)
        print ('menu, ', self.menu)
        
        
def getQuery(data): 
    global food 
    
    #with open("./input.json") as f:
    #    data = json.load(f)
    
    food = data[0]
    for i in range (1, len(data)):
        restaurant = data[i]
        print (restaurant["restaurantName"])
        new = Restaurant(restaurant["restaurantName"], restaurant["address"])
        new.distance = restaurant['distance']
        new.lat = restaurant['lat']
        new.lng = restaurant['lng']
        new.rating = restaurant['rating']
        
        
        try: 
            getPlaceUrl(new.name, new.address)
            menu = getMenu(new.name)
            new.menu = menu 
            with open(str(new.name) + 'data.json', 'w+', encoding='utf-8') as outfile:
                json.dump(menu, outfile, indent=4, ensure_ascii=False)
            results = getPrices(new)
            restaurant['prices'] = (results)
            busy = (getBusyTimes(new.name, new.lat, new.lng))
            restaurant['popularTimes'] = (busy)

        except Exception as ex:
            print ('line 66 ', ex)
            continue 
        '''
        results = getPrices()
        restaurant['prices'] = (results)
        busy = (getBusyTimes(new.name, new.lat, new.lng))
        restaurant['popularTimes'] = (busy)
        '''
    return (data)

def sendQuery(data): 
    with open('output.json', 'w+', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
    
    

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    # POST request
    if request.method == 'POST':
        print('Incoming..')

        # asjson = json.dumps(request.get_json())
        asjson = request.get_json()[1]
        data = getQuery(asjson)
        print(type(asjson))  # parse as JSON
        print(asjson)
        return jsonify(data)

    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers

def getPlaceUrl(name, address):
    words = address.split(' ')
    words += name.split(' ')
    base_url = "https://www.google.com/search?q="
    for word in words: 
        base_url += '+' + word
    base_url += '+' + "site:ubereats.com"
    driver = webdriver.Chrome(executable_path="./chromedriver.exe")
    
    counter = 10
    for i in range (0, counter):
        try: 
            driver.get(base_url)
            temp_urls = driver.find_element_by_xpath("/html/body/div[7]/div[1]/div[9]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]").find_elements_by_tag_name("a")
                    
            break
        except Exception as ex:
            try: 
                print ('error 1')
                temp_urls = driver.find_element_by_xpath("/html/body/div[7]/div[1]/div[8]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]").find_elements_by_tag_name("a")
            except: 
                print("error ", ex)
            
    for url in temp_urls:
        out_file = open("temp_urls.txt", "a")
        url = url.get_attribute("href")
        
        print (url)
        if ((("google" in url) == False) and (("webcache" in url) == False)): 
            print ('string ', url)
            out_file.write(str(url) + "\n")

    out_file.close()

    lines_seen = set()  # holds lines already seen
    out_file = open(name + "_urls.txt", "w+")
    for line in open("temp_urls.txt", "r"):
        if line not in lines_seen:  # not a duplicate
            out_file.write(line)
            lines_seen.add(line)
    out_file.close()

    os.remove("temp_urls.txt")

def getMenu(place): 
    result = []
    
    file = open(place + '_urls.txt', 'r')
    lines = file.readlines()
    
    for line in lines:
        try:  
            result.append(menu_scraper.scrape_menu(line))
        except Exception as ex: 
            print ("didn't work ", ex)
            continue
    
    return result

def getPrices(place): #place
    global food 
    food = 'ribeye'
    menu = place.menu
    #with open("./Texas Roadhousedata.json") as f:
     #   menu = json.load(f)
        
    results = {
        'item': []
        } 
    
    
    
    
    for category in (menu[0]['menu']): 
        for catName in category: 
            for item in (category[catName]):
                print (item['name'])
                if food.lower() in item['name'].lower(): 
                    dish = {
                        'name' : item['name'],
                        'price' : item['price']
                        }
                    results['item'].append(dish)
    print (results)
    return results 

def getBusyTimes(name, lat, lng):
    a = populartimes.get("AIzaSyC9OUVOA30j_zhlh0JLvkbp-PQJslXnqUA", [name], (lat + 0.001, lng + 0.001), (lat - 0.001, lng - 0.001))
    result = -1
    for location in a: 
        if (name.lower() in location['name'].lower()):
            times = (location['populartimes'])
            for day in times: 
                if day['name'] == datetime.datetime.now().strftime("%A"): 
                    result = (day['data'][datetime.datetime.now().hour])
                    break
    return result
    
def main(): 
    global restaurants
    
    #getQuery()
    getQuery()


if __name__ == "__main__":
    main() 