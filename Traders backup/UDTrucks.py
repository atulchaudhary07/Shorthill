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
# path = r'packages/chromedriver'
# driver = webdriver.Chrome(executable_path=path, options=chrome_options)
URL = "https://www.udtrucks.com"
robot = bot(URL)
(soup,code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
subclass=soup.find_all("div",{"class":"promo row align-middle"})
sub_urls=[]
for subIndex in subclass:
    subclass_href=subIndex.find("a").get("href").replace("//","").strip()
    # print(subclass_href)
    sub_urls.append(subclass_href)
tempUrl=OrderedSet(sub_urls)
for ProdUrl in tempUrl:
    NavUrls="https://"+ProdUrl
    # print(NavUrls)
    (nvsoup,code) = robot.get_content(NavUrls, {"method": "get", "bs4": "y"})
    # print(nvsoup)
    fets=[]
    imges=[]
    product_name=nvsoup.find_all("span",{"class":"product-type-product-name active"})
    for mod in product_name:
        model=mod.text
        try:
            Subcat=nvsoup.find("div",{"class":"sub-nav-title show-for-large"}).text
        except:
            pass

        try:
            # features
            feat_cont=nvsoup.find_all("div",{"class":"features-container"})
            for fetIndex in feat_cont:
                try:#hi
                    h1=fetIndex.find("h1").text
                    fets.append(h1)

                except:
                    pass
                try:#ptag
                    fetptag=fetIndex.find("p").text
                    fets.append(fetptag)
                    # print(fetptag)
                except:
                    pass

        except:
            pass

        try:
            #bar_icon_text
            barclass=nvsoup.find("div",{"class":"icon-bar product-heading-icons"}).find_all("a")
            for brAtag in barclass:
                fets.append(brAtag.text)

        except:
            pass
        try:
            # imges
            imgecont=nvsoup.find("div",{"id":"product_details_view"}).find_all("img")
            for imgIndex in imgecont:
                imgsrc="https://www.udtrucks.com"+imgIndex.get("src")
                if re.search(r'(?i).jpg', imgsrc):
                    imges.append(imgsrc)
        except:
            pass

        try:
            # spec
            specblock=nvsoup.find_all("div",{"class":"specs-block"})
            for spcInd in specblock:
                specname= spcInd.find("div",{"class":"detail-category"}).text.strip()
                specvalue=spcInd.find("div",{"class":"detail-value"}).text.strip()
                # print(specname)
                # print(specvalue)
                if len(specvalue) > 0:
                    if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Cooling|Transmission|Power|Torque', specname):
                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                    elif re.search(r'(?i)Weight|Load', specname):
                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"weights")
                    elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure', specname):
                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"hydraulics")
                    elif re.search(r'(?i)Length|Height|Radius|Track|Width', specname):
                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"dimensions")
                    else:
                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"operational")
                else:
                    pass
        except:
            pass

        ImgLst = OrderedSet(imges)
        for ImgIndex in ImgLst:
            robot.fetch_img_manual(ImgIndex)
        TempFeatList = OrderedSet(fets)
        for FetIndex in TempFeatList:
            robot.Features(FetIndex)

        desc="Trucks"+" "+ model
        robot.ObjectID(model)
        robot.MasterCategory("Trucks")
        robot.SubCategory(Subcat)
        robot.ProductUrl(NavUrls)
        robot.Description(desc)
        robot.Country("US")
        robot.ManufacturerName("UD Trucks")
        robot.make_json()
robot.destroy()







