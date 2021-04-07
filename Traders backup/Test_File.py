from selenium import webdriver
from bs4 import BeautifulSoup
import requests, json, time
from ordered_set import OrderedSet
from selenium.webdriver.chrome.options import Options
import pdfkit
import sys
import re

from selenium.webdriver.common.keys import Keys

try:
    from packages import bot
except:
    sys.path.insert(0, '../')
    from packages.Crawler import bot
#
chrome_options = Options()
chrome_options.add_argument("--headless")
path = r'packages/chromedriver'
driver = webdriver.Chrome(executable_path=path, options=chrome_options)
# driver = webdriver.Chrome(executable_path=path)
# counter=0
# robot = bot(URL)
# (soup, code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
URL="https://www.fleetwoodrv.com/models/discovery-lxe-2021"
driver.get(URL)
time.sleep(5)
models=driver.find_element_by_id("floorplans").find_element_by_xpath('//div[@class="slider-controls text-center flex flex-wrap justify-center"]').find_elements_by_xpath('//div[@class="w-1/3 md:w-auto p-3"]')
# calloutclass=driver.find_element_by_id("floorplans").find_elements_by_xpath('//nav[@class="callout-nav"]')
# for calloutIndex in range(len(calloutclass)):

# counter=0
# for mods in models:
#     model=mods.text
#     try:
#         # calloutclass=driver.find_elements_by_xpath('//nav[@class="callout-nav"]')
#         try:
#             src_360=calloutclass[calloutIndex].find_element_by_xpath('//a[@class="callout-nav-link block uppercase tracking-wider text-center text-xs w-32"]').get_attribute("href")
#             print(src_360)
#         except:
#             pass
#         try:
#             all_options=calloutclass[calloutIndex].find_element_by_xpath('//a[@class="callout-nav-link uppercase tracking-wider text-center text-xs block w-32"]').get_attribute("href")
#             print(all_options)
#         except:
#             pass
#     except:
#         pass
#     print(counter)
#     counter=counter+1
    # print(counter)

# script=driver.find_element_by_id("mainPage").find_element_by_xpath('//a[@class="callout-nav-link block uppercase tracking-wider text-center text-xs w-32"]').get_attribute("href")
# driver.execute_script(script)
# couter=0


