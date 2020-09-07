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

URL = "https://www.airstream.com"
# path = r'packages/chromedriver'
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(executable_path=path, options=chrome_options)
# driver.get(URL)
# time.sleep(10)
robot = bot(URL)
(soup,code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
nav_list=soup.find("ul",{"class":"m-header-nav-list"}).find_all("li", recursive=False)[:-1]
for liIndex in nav_list:
    All_trailers=liIndex.find("a").get("href")
    # category=liIndex.find("a").text
    (Navsoup, code) = robot.get_content(All_trailers, {"method": "get", "bs4": "y"})
    product_grid=Navsoup.find("section",{"id":"product-grid"}).find_all("div",{"class":"col-md-6 col-lg-4 card card-product text-center"})
    for mod in product_grid:
        # product_img=mod.find("div",{"class":"card-product-img"}).find("img").get("data-src")
        # robot.fetch_img_manual(product_img)
        # subcat=mod.find("h3").text
        # try:
        #     msrp=mod.find("p",{"class":"p3 setone mb-0"}).text
        # except:
        #     pass
        nav_src=mod.find("a").get("href")
        (product_page, code) = robot.get_content(nav_src, {"method": "get", "bs4": "y"})
        # print(product_page)
        Images_list=[]
        option_list=[]
        Feature_list=[]
        # Video_list=[]

        # try:
        #     year=
        # except:
        #     pass

        try:
            #tabs
            tabs=product_page.find("ul",{"class":"m-subnav-nav-list"}).find_all("a")[1:-1]
            for tabsIndex in tabs:
                tabs_src=tabsIndex.get("href")
                (tabcont, code) = robot.get_content(tabs_src, {"method": "get", "bs4": "y"})
                try:
                    #imges
                    img=tabcont.find("div",{"class":"m-gallery-grid-wrapper"}).find_all("div",{"class":"m-gallery-grid-item image-rectangle"})
                    for ImgIndex in img:
                        Images_list.append(ImgIndex.find("img").get("data-gallery-index-img-src"))
                except:
                    pass
                try:
                    # feat
                    feats_cloud=tabcont.find_all("section",{"class":["m-text-media-split pt-md pb-0 bg-cloud night","m-text-media-split pt-md pb-md bg-cloud night"]})
                    for IndexFetcloud in feats_cloud:
                        try:
                            contentInside=IndexFetcloud.find("div",{"class":"content"}).text
                            Feature_list.append(contentInside)
                        except:
                            pass

                except:
                    pass
                try:
                    # feature_grid
                    feature_grid=tabcont.find("section",{"id":"features-grid"}).find_all("div",{"class":"col-sm-6 col-lg-4 card card-feature"})
                    for girdIndex in feature_grid:
                        # print(girdIndex)
                        girdtext=girdIndex.text.strip()
                        Feature_list.append(girdtext)
                        grid_fet_img=girdIndex.find("div",{"class":"image-square"}).find("a").get("href")
                        Images_list.append(grid_fet_img)

                except:
                    pass
                try:
                    # Slider
                    fets_slide=tabcont.find("section",{"class":"m-text-media-split-carousel pt-md pb-sm bg-white night"})
                    for fet_slide_index in fets_slide:
                        try:
                            text_fet_slide=fet_slide_index.find_all("div",{"class":"m-text-media-split-carousel-slide-text"})
                            for text_index in text_fet_slide:
                                h3Tag=text_index.find("h3",{"class":"mt-0"}).text.strip()
                                ptag=text_index.find("p",{"class":"p2"}).text.strip()
                                Feature_list.append(h3Tag)
                                Feature_list.append(ptag)

                        except:
                            pass
                        try:
                            Slide_imges=fet_slide_index.find_all("div",{"class":"image-rectangle"})
                            for index_imge_slide in Slide_imges:
                                Images_list.append(index_imge_slide.find("img").get("data-src"))

                        except:
                            pass
                except:
                    pass

                try:
                    # spec:
                    specs_table=tabcont.find("section",{"id":"specs-table"}).find("tbody").find_all("tr")
                    for trindex in specs_table:
                        specname=trindex.find_all("td")[0].text.strip()
                        specvalue=trindex.find_all("td")[1].text.strip()
                        # print(specname)
                        # print(specvalue)
                        if re.search(r'(?i)n/a|N/A|no|No|-', specvalue):
                            pass
                        elif re.search(r'(?i)STD', specvalue):
                            Feature_list.append(specname)
                        elif re.search(r'(?i)Optional|Option|OPT', specvalue):
                            option_list.append(specname)
                        else:
                            if len(specvalue) > 0:
                                if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Cooling', specname):
                                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                                elif re.search(r'(?i)Operating|Pressure|Capacity|Fuel|tank|Speed', specname):
                                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"operational")
                                elif re.search(r'(?i)Length|Height||Radius|Track|Width|Load', specname):
                                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"dimensions")
                                elif re.search(r'(?i)Weight|Load', specname):
                                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "weights")
                                elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure', specname):
                                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"hydraulics")
                                else:
                                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "other")
                            else:
                                pass
                except:
                    pass
        except:
            pass
        try:
            tabs2 = product_page.find("ul", {"class": "m-subnav-nav-list"}).find_all("a")[1:-1]
            for tabsIndex2 in tabs2:
                floor_plan=tabsIndex2.text.strip()
                if re.search(r'(?i)Floor Plans',floor_plan):
                    Floor_tab = tabsIndex2.get("href")
                    (floorcont, code) = robot.get_content(Floor_tab, {"method": "get", "bs4": "y"})
                    fl_plan=floorcont.find("section",{"id":"floorplan-grid"}).find_all("div",{"class":"bg-white p-5 text-center card-floorplan-lower"})
                    for PlnIndex in fl_plan:
                        # print(PlnIndex)
                        model=PlnIndex.find("h2",{"class":"mb-0 card-floorplan-name"}).text.strip()
                        category = liIndex.find("a").text
                        subcat = mod.find("h3").text

                        try:
                            product_img = mod.find("div", {"class": "card-product-img"}).find("img").get("data-src")
                            robot.fetch_img_manual(product_img)
                        except:
                            pass

                        try:
                            msrp=PlnIndex.find("h4",{"class":"stone nh-bold"}).text.strip()
                            robot.Msrp(msrp)
                        except:
                            pass
                        try:
                            dec=product_page.find("section",{"class":"m-intro-copy bg-white night pt-md pb-sm"}).find("p").text
                            robot.Description(dec)

                        except:pass

                        TempFeatList = OrderedSet(Feature_list)
                        for FetIndex in TempFeatList:
                            robot.Features(FetIndex)
                        ImgLst = OrderedSet(Images_list)
                        for ImgIndex in ImgLst:
                            robot.fetch_img_manual(ImgIndex)
                        TempOpList = OrderedSet(option_list)
                        for OpIndex in TempOpList:
                            robot.Options(OpIndex)
                        robot.ObjectID(model)
                        robot.SubCategory(subcat)
                        robot.MasterCategory(category)
                        robot.ProductUrl(nav_src)
                        robot.Country("US")
                        robot.ManufacturerName("Airstream")
                        robot.make_json()
                else:
                    pass

        except:
            pass
robot.destroy()


