from selenium import webdriver
from bs4 import BeautifulSoup
import requests, json,time,re
from selenium import webdriver
from ordered_set import OrderedSet
import sys
import re
from selenium.webdriver.chrome.options import Options
# path= r"packages/phantomjs"
try:
    from packages import bot
except:
    sys.path.insert(0, '../')
    from packages.Crawler import bot


import re, datetime, sys, os, time
from unidecode import unidecode
import requests, json, time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from ordered_set import OrderedSet

try:
    from packages import bot
except:
    sys.path.insert(0, '../')
    from packages.Crawler import bot

URL = "https://www.deere.com/en/scraper-systems/scraper-special-tractors/9570rt-scraper-special-tractor/"
# path = r'packages/chromedriver'
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(executable_path=path, options=chrome_options)
# driver.get(URL)
# driver.page_source
# time.sleep(10)
robot = bot(URL)
(soup,code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
# print(soup)
try:
    # feature
    fet_class = soup.find("div", {"data-action": "expandCollapseComponent"}).find_all("p")
    for ptag in fet_class:
        ptag_text = ptag.text.splitlines()
        for Index_P_tag in ptag_text:
            print(Index_P_tag)
    #             if re.search(r'(?i)Optional',Index_P_tag):
    #                 Option_lis.append(Index_P_tag)
    #             else:
    #                 feats_lis.append(Index_P_tag)
    #
except:
    pass