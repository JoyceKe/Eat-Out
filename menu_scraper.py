# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 00:15:24 2021

@author: ellix
"""

from selenium import webdriver


def scrape_menu(url):
    driver = webdriver.Chrome(executable_path="./chromedriver.exe")
    driver.maximize_window()
    driver.get(url)

    # ===== Header details =====
    detail = ''
    rating = ''
    num = ''

    try:
        detail = driver.find_element_by_xpath("/html/body/div/div/main/div[1]/div/div/div[2]/div/div[2]/div[1]").text
    except:
        detail = ''

    try:
        rating = driver.find_element_by_xpath(
            "/html/body/div/div/main/div[1]/div/div/div[2]/div/div[2]/div[2]/div[1]").text
    except:
        rating = 'N/A'

    try:
        num = driver.find_element_by_xpath(
            "/html/body/div/div/main/div[1]/div/div/div[2]/div/div[2]/div[2]/div[3]").text
    except:
        num = '(0)'
      
    counter = 15
    for i in range (0, counter): 
        try: 
            temp = driver.find_element_by_xpath("/html/body/div/div/main/div[3]/div/div[4]/div[3]").text
            break 
        except Exception as ex: 
            try: 
                temp = driver.find_element_by_xpath("/html/body/div/div/main/div[3]/div/div[3]/div[3]").text #/div[1]/div[2]/div[2]/h1
                print ('first exception', ex)
            except Exception as ex2:     
                print ('second exception ', ex2)
    print (temp)
    restaurant = {
        'title': temp, #/html/body/div/div/main/div[1]/div/div/div[2]/div/div[2]/h1
        'detail': detail,
        'rating': rating,
        'num_reviews': num,
        'menu': []
    }

    # ===== Menu =====
    list_item_element = driver.find_element_by_xpath("/html/body/div/div/main/div[5]/ul").find_element_by_tag_name("li")
    menu = driver.find_element_by_xpath("/html/body/div/div/main/div[5]/ul").find_elements_by_class_name(
        list_item_element.get_attribute("class"))

    name = ''
    description = ''
    status = ''
    price = ''
    img_url = ''
    
    for x in range(len(menu) - 1):
        while True: 
            category = driver.find_element_by_xpath("/html/body/div/div/main/div[5]/ul/li[" + str(x + 1) + "]/h2").get_attribute('textContent')
            print (category)
            if len(category) > 0:
                break
        restaurant['menu'].append({
            category: []
        })
        section = driver.find_element_by_xpath(
            "/html/body/div/div/main/div[5]/ul/li[" + str(x + 1) + "]/ul").find_elements_by_tag_name("li")

        for y in range(len(section)):

            # Get Product Name
            try:
                name = str(driver.find_element_by_xpath(
                    "/html/body/div/div/main/div[5]/ul/li[" + str(x + 1) + "]/ul/li[" + str(
                        y + 1) + "]/div/div/div/div/div[1]/h4").get_attribute('textContent'))
            except:
                name = ''

            # Get Product Description
            try:
                description = str(driver.find_element_by_xpath(
                    "/html/body/div/div/main/div[5]/ul/li[" + str(x + 1) + "]/ul/li[" + str(
                        y + 1) + "]/div/div/div/div/div[2]").get_attribute('textContent'))
            except:
                description = ''

            # Get Product Price
            try:
                price = str(driver.find_element_by_xpath(
                    "/html/body/div/div/main/div[5]/ul/li[" + str(x + 1) + "]/ul/li[" + str(
                        y + 1) + "]/div/div/div/div/div[3]").get_attribute('textContent'))

                if price == description:
                    description = ''

                if "Sold" in price:
                    status = "Sold out"
                    price = "$" + price.split("$", 1)[1]
                else:
                    status = "In stock"

            except:

                if "$" in description:
                    price = description
                    description = ''
                else:
                    price = ''

            # Get Image URL
            try:
                img_url = str(driver.find_element_by_xpath(
                    "/html/body/div/div/main/div[5]/ul/li[" + str(x + 1) + "]/ul/li[" + str(
                        y + 1) + "]/a/div/div[2]/img").get_attribute("src"))
            except:
                img_url = ''

            restaurant['menu'][x][category].append({
                'name': name,
                'description': description,
                'price': price,
                'status': status,
                'img_url': img_url
            })

    return restaurant