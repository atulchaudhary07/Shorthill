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

chrome_options = Options()
chrome_options.add_argument("--headless")
path = r'packages/chromedriver'
driver = webdriver.Chrome(executable_path=path, options=chrome_options)
URL = "https://sennebogen-na.com/product/material-handlers/"
robot = bot(URL)
driver.get(URL)
time.sleep(3)
resonse=driver.page_source
soup=BeautifulSoup(resonse,"html.parser")
prod_container=soup.find("div",{"class":"model_list_view"}).find_all("h3")
for indexProd in prod_container:
    product_url=indexProd.find("a").get("href")
    # subcat=indexProd.find("a").text
    (pro_page, code) = robot.get_content(product_url, {"method": "get", "bs4": "y"})
    Subcategry=pro_page.find("h1").find("div",{"class":"product-category uk-h4"}).text

    Series=pro_page.find("h1").find("span",{"class":"series"}).text
    model_name=pro_page.find("h1").text.replace(Subcategry,"")
    Allimg=[]
    Allfets=[]
    videos=[]
    # print(model_name)
    try:
        # Image
        gallry=pro_page.find("div",{"class":"product-gallery"}).find_all("img")
        for imgIndex in gallry:
            Allimg.append("https://sennebogen-na.com"+imgIndex.get("src"))
    except:
        pass
    try:
        # Spec
        specont=pro_page.find("table",{"class":"product-table"}).find("tbody").find_all("tr")
        for spcIndex in specont:
            specname=spcIndex.find_all("td")[0].text
            try:
                specvalue=spcIndex.find_all("td")[-1].find("span").text
                if re.search(r'(?i)n/a|N/A', specvalue):
                    pass
                else:
                    if len(specvalue) > 2:
                        if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Torque|Power', specname):
                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                        elif re.search(r'(?i)Operating|Pressure|Capacity|Fuel|tank|Speed|force', specname):
                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "operational")
                        elif re.search(r'(?i)Length|Height|Radius|Track|Width|Digging|Range', specname):
                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "dimensions")
                        elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure|Load', specname):
                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "hydraulics")
                        else:
                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "operational")
                    else:
                        pass
            except:
                specvalue = spcIndex.find_all("td")[-1].text
                if re.search(r'(?i)n/a|N/A', specvalue):
                    pass
                else:
                    if len(specvalue) > 2:
                        if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Torque|Power', specname):
                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                        elif re.search(r'(?i)Operating|Pressure|Capacity|Fuel|tank|Speed|force', specname):
                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "operational")
                        elif re.search(r'(?i)Length|Height|Radius|Track|Width|Digging|Range', specname):
                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "dimensions")
                        elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure|Load', specname):
                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "hydraulics")
                        else:
                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "operational")
                    else:
                        pass
    except:
        pass

    try:
        # dec
        product_dec=pro_page.find("div",{"class":"financing"}).text.strip().title()
        robot.Description(product_dec)
    except:
        pass

    try:
        #product_feat
        prod_fet=pro_page.find_all("div",{"class":"highlights"})
        for indexfet in prod_fet:
            # print(indexfet)
            h3=indexfet.find("h3").text.title()
            desc=indexfet.find("div",{"class":"highlight-description"}).text.title()
            Allfets.append(h3)
            Allfets.append(desc)
    except:
        pass
    try:
        pdf_direct=pro_page.find("div",{"class":"direct-download"}).find("input",{"id":"mail_download_link"}).get("value")
        if re.search(r'(?i)https:', pdf_direct):
            robot.fetch_pdf_manual(pdf_direct)

            # print(cttmplink)
        else:
            pdf_link = "https://sennebogen-na.com/" + pdf_direct
            # catlinks_lis.append(catLink)
            robot.fetch_pdf_manual(pdf_link)
    except:
        pass
    try:

        #images
        higlitImge=pro_page.find_all("div",{"class":"highlights"})
        for indexImge in higlitImge:
            img_tag=indexImge.find_all("img")
            for Imgindextg in img_tag:
                src=Imgindextg.get("src")
                if len(src)>3:
                    Allimg.append(src)
    except:
        pass
    try:
        # Videos
        vid=pro_page.find_all("a",{"class":"fancybox-youtube"})
        for VidIndex in vid:
            src_vid=VidIndex.get("href")
            if len(src_vid)>3:
                videos.append(src_vid)
    except:
        pass
    ImgLst = OrderedSet(Allimg)
    for ImgIndex in ImgLst:
        robot.fetch_img_manual(ImgIndex)
    TempFeatList = OrderedSet(Allfets)
    for Indexfet in TempFeatList:
        robot.Features(Indexfet)
    tempVideoList=OrderedSet(videos)
    for IndexVid in tempVideoList:
        robot.fetch_videos(IndexVid)
    robot.MasterCategory("Cranes")
    robot.SubCategory(Subcategry)
    robot.ObjectID(model_name)
    robot.ProductUrl(product_url)
    robot.Country("US")
    robot.ManufacturerName("Sennebogen")
    robot.make_json()
robot.destroy()
driver.close()




