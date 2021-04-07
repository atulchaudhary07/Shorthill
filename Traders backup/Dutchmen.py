from selenium import webdriver
from bs4 import BeautifulSoup
import requests, json, time
import dload
from ordered_set import OrderedSet
from selenium.webdriver.chrome.options import Options
import sys
import re
try:
    from packages import bot
except:
    sys.path.insert(0, '../')
    from packages.Crawler import bot

chrome_options = Options()
chrome_options.add_argument("--headless")
path = r'packages/chromedriver'
driver = webdriver.Chrome(executable_path=path, options=chrome_options)
URL = "https://www.dutchmen.com"
# robot = bot(URL)
driver.get(URL)
time.sleep(5)
print(driver.page_source)