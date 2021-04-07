from selenium import webdriver #selenium webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as Ec
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import csv
import time
chrome_options = Options()
chrome_options.add_argument("--headless")
path = r'packages/chromedriver'
driver = webdriver.Chrome(executable_path=path, options=chrome_options)
URL = "https://sennebogen-na.com/product/material-handlers/"
driver.get(URL)
header = []
time.sleep(3)
linkdata = []
namedata = []
df = pd.DataFrame({'Product_Name':[''],'Category':[''],'Product Url':[''],'Image':[''],'Description':['']})
for i in range(1,52):
    link = driver.find_element_by_xpath('/html/body/div[4]/div/section/div/main/div/article/div[3]/div[2]/div/div[{}]/div/h3/a'.format(i))# Name of the Product
    name = link.text
    namedata.append(name)

    link = link.get_attribute('href')

    linkdata.append(link)
print(linkdata)
for i in range(0,len(linkdata)):
    driver.get(linkdata[i])
    print(namedata[i])
    print(linkdata[i])
    category = driver.find_element_by_xpath('/html/body/div[4]/div/section/div/main/div/article/div[2]/h1/div').text  # category of the product

    print(category)
    image = driver.find_element_by_xpath('/html/body/div[4]/div/section/div/main/div/article/div[2]/div[1]/div/ul/li/img')  # image ur
    image = image.get_attribute('src')

    print(image)
    discription = driver.find_element_by_css_selector('div.financing>p').text

    print(discription)
    df = df.append(
        {'Product_Name': namedata[i], 'Category': category, 'Product Url': linkdata[i], 'Image': image, 'Description': discription},
        ignore_index=True)



df.to_csv('C:/Users/yash/Pictures/Witcher/ final.csv')




