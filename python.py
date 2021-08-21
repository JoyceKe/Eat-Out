# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 23:53:35 2021

@author: ellix
"""

from selenium import webdriver


class Restaurant(): 
    def __init__(self, name, address, price):
        self.name = name
        self.address = address 
        self.price = price 
        self.distance = 0 
        
def cockroach(): 
    food = 'ribs'
    places = ['mcdonalds']
    addresses = ['123 ford drive, oakville, ontario, canada']
    return food, places, addresses

def getPrices(place, food): 
    return 0 

def main(): 
    food, places, addresses = cockroach()
    restaurants = []
    for x in range (0, len(places)): 
        location = Restaurant(places[x], addresses[x], getPrices(places[x], food))
        restaurants.append(location)
    
    
if __name__ == "__main__":
    main() 