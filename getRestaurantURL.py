# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 17:11:28 2021

@author: ellix
"""

from selenium import webdriver
import os


def scrape_restaurants():
    base_url = "https://www.google.com/search?q=ubereats+1500+Upper+Middle+Rd+W%2C+Oakville%2C+ON+L6M"
    driver = webdriver.Chrome(executable_path="./chromedriver.exe")

    while True:
        try: 
            driver.get(base_url)
            temp_urls = driver.find_element_by_xpath("/html/body/div[7]/div[1]/div[8]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]").find_elements_by_tag_name("a")
                    
            break
        except Exception as ex:
            print("error ", ex)
            
    for url in temp_urls:
        out_file = open("temp_urls.txt", "a")
        url = url.get_attribute("href")
        
        if ("https://www.ubereats.com/" in url) and (("webcache" in url) == False): 
            print ('string ', url)
            out_file.write(str(url) + "\n")

    out_file.close()

    lines_seen = set()  # holds lines already seen
    out_file = open("restaurant_urls.txt", "w+")
    for line in open("temp_urls.txt", "r"):
        if line not in lines_seen:  # not a duplicate
            out_file.write(line)
            lines_seen.add(line)
    out_file.close()

    os.remove("temp_urls.txt")
    
scrape_restaurants()