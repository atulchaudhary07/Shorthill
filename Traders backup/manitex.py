from selenium import webdriver
from bs4 import BeautifulSoup
import requests, json, time
from ordered_set import OrderedSet
from selenium.webdriver.chrome.options import Options
import sys
import re
try:
    from packages import bot
except:
    sys.path.insert(0, '../')
    from packages.Crawler import bot

# chrome_options = Options()
# chrome_options.add_argument("--headless")
path = r'packages/chromedriver'
driver = webdriver.Chrome(executable_path=path)
# driver = webdriver.Chrome(executable_path=path, options=chrome_options)
URL = "https://www.manitex.com/products.aspx?"
driver.get(URL)
driver.implicitly_wait(5)
response=driver.page_source
soup=BeautifulSoup(response,"html.parser")
mobile_menu=soup.find("div",{"class":"megamenu_mobile visible-xs visible-sm"}).find_all("ul",{"class":"level_1"})[-1]
Product_menu=mobile_menu.find_all("li",recursive=False)[1].find("ul",{"class":"level_3"}).find_all("a")
# Index = 0
# butn_list=[]

for catlink in Product_menu:
    categoryLink ="https://www.manitex.com/"+catlink.get("href").replace(' ','%20')
    driver.get(categoryLink)
    driver.implicitly_wait(5)
    Imge_button=driver.find_elements_by_xpath('//input[@type="image"]')
    for Btlist in Imge_button:
        inner_elemnts=Btlist.find_element_by_id("CatPanel").find_elements_by_tag_name("b")
        # for inner_elemnts in inner_elemnts:
        #     inner_elemnts.find_element_by_tag_name("a").click()
        # print(Btlist)
        # Btlist.click()
        # driver.implicitly_wait(5)
        # driver.back()
        # driver.implicitly_wait(5)

        # butn_list.append(Btlist.get_attribute("onclick"))

# while len(butn_list)>Index:
#     butn_list[Index].click()
#     time.sleep(3)
#     driver.back()
#     Index = Index + 1
#     time.sleep(2)
    # for onlickPath
    # print(categoryLink)
    # driver.get(categoryLink)
    # driver.implicitly_wait(5)
    # prod = driver.page_source
    # Prodsoup = BeautifulSoup(prod, "html.parser")
    # main= Prodsoup.find("main").find_all("h5")
    # for index in main:
    #     link =index.find("input",{"type":"image"}).get("onclick").split(",")[-3].strip().replace('"',"")
    #     sucat_link="https://www.manitex.com/" + link
    #     driver.get(sucat_link)

        # driver.implicitly_wait(5)
        # sucatPageSoup=BeautifulSoup(driver.page_source, "html.parser")
        # h3=sucatPageSoup.find_all("h3",{"class":"media-heading"})
        # for i in h3:
        #     print(i)
        # print(sucatPageSoup)




    


