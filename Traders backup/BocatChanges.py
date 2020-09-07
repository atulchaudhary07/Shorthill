import re, datetime, sys, os, time
from unidecode import unidecode
import requests, json, time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from ordered_set import OrderedSet
file= "/Users/atulchaudhary/PycharmProjects/Headless/BobCatTestCode.json"
f = open(file)
data= json.load(f)
Unique_data=[]
for nodes in data:
    Unique_data.append(nodes)
newdata=OrderedSet(Unique_data)
print(newdata)


    # New_model_name=nodes['general']["model"].replace("Bobcat","").replace("Company","").strip()
    #
    # subcat=nodes['general']["subcategory"].strip()
    # # new_model=model_name.replace("Compact Track Loader","").replace("Skid-Steer Loader","").replace("All-Wheel Steer Loader","").replace("Small Articulated Loader","").replace("Compact Excavator","").replace("Sub-Compact Tractor","").replace("Utility Vehicle","").replace("Excavator","").replace("Compact Tractor","")
    # nodes['general']["model"]=New_model_name
# with open('BobcatAttachmentData.json', 'w') as f:
#     json.dump(data, f)
