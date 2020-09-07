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

URL = "https://www.felling.com/"

robot = bot(URL)
(soup,code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
nav=soup.find("div",{"id":"header"}).find("ul",{"id":"menu-nav"}).find("li",{"id":"menu-item-12"}).find("ul",{"class":"sub-menu"}).find_all("li",recursive=False)[:3]
for nvIndex in nav:
    # print(nvIndex)
    Anchor=nvIndex.find_all("li")
    for indexAnchor in Anchor:
        # subcat=indexAnchor.find("a").text
        Nav_url=indexAnchor.find("a").get("href")
        (navpage, code) = robot.get_content(Nav_url, {"method": "get", "bs4": "y"})
        try:
            # model_name=
            # for Modindex in model_name:
            #     print(Modindex)
            aTag=navpage.find("div",{"class":"entry-content"}).find_all("a",{"target":"_blank"})
            for aIndex in aTag:
                model_name=aIndex.text.strip()
                model_list = []
                if re.search(r'(?i)Galvanizing|Paint|Ramps|Option|View|Hot Dip|Finish|TSA|Narrow Neck|Options|Gas Engine Powered|Felling Tarp System|Questions|Pan Tilt|Series',model_name):
                    pass
                else:
                    if len(model_name)>1:
                        model_list.append(model_name)
                Model_set=OrderedSet(model_list)
                for modListIndex in Model_set:
                    model=modListIndex
                    # print(model)
                    Imges_list=[]
                    video_list=[]
                    Ptag_all=[]
                    declist=[]
                    subcat = indexAnchor.find("a").text

                    try:
                        pdf=aIndex.get("href")
                        robot.fetch_pdf_manual(pdf)
                    except:
                        pass

                    try:
                        img=navpage.find("div",{"id":"content"}).find_all("img")
                        for imgIndex in img:
                            # title=imgIndex.get("title")
                            imgsrc = imgIndex.get("src")
                            if len(imgsrc)>0:
                                # print(imgsrc)
                                Imges_list.append(imgsrc)
                            # if re.search(str(model),imgsrc):
                            #     print(model)
                                # print(imgsrc)

                            # print(imgsrc)
                    except:pass
                    try:
                        vide=navpage.find("div",{"id":"content"}).find_all("iframe")
                        for iframIndex in vide:
                            video_src=iframIndex.get("src")
                            video_list.append(video_src)

                    except:
                        pass
                    try:
                        decH4=navpage.find("div",{"id":"content"}).find("h2").text
                        declist.append(decH4)


                    except:pass

                    try:
                        dec=navpage.find("div",{"id":"content"}).find("p").text
                        if len(dec)>3:
                            declist.append(dec)
                        else:
                            dec="Felling Trailer"+" "+model
                            declist.append(dec)

                        # robot.Description(dec)
                    except:
                        pass

                    try:
                        tempdec=OrderedSet(declist)
                        decs=" ".join(tempdec)
                        robot.Description(decs)

                    except:
                        pass
                    try:
                        # ptag
                        ptg=navpage.find("div",{"id":"content"}).find_all("p")[1:]
                        for pgIndex in ptg:
                            pgtext=pgIndex.text.strip()
                            Ptag_all.append(pgtext)

                    except:pass

                    tempPtag=OrderedSet(Ptag_all)
                    for tagAllIndex in tempPtag:
                        if re.search(r'(?i)Optional|Option', tagAllIndex):
                            robot.Options(tagAllIndex)
                        else:
                            robot.Features(tagAllIndex)

                    ImgLst = OrderedSet(Imges_list)
                    for ImgIndex in ImgLst:
                        if re.search(r'(?i)0008S|FTS_FELLING|logo', ImgIndex):
                            pass
                        else:
                            robot.fetch_img_manual(ImgIndex)
                    TempVdList = OrderedSet(video_list)
                    for vdIndex in TempVdList:
                        robot.fetch_videos(vdIndex)
                    robot.ObjectID(model)
                    robot.SubCategory(subcat)
                    robot.MasterCategory("Trailers")
                    robot.ProductUrl(Nav_url)
                    robot.Country("US")
                    robot.ManufacturerName("Felling Trailer")
                    robot.make_json()
        except:
            pass
robot.destroy()

