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

URL = "https://www.dixiechopper.com/"
# path = r'packages/chromedriver'
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(executable_path=path, options=chrome_options)
# driver.get(URL)
# time.sleep(10)
robot = bot(URL)
(soup,code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
nav=soup.find("ul",{"class":"nav navbar-nav main-nav"}).find("li").find_all("a")
nav_link=[]
series=[]
try:
    for atag in nav:
        if atag.get("href") is "#":
            pass
        else:
            nav_link.append(atag.get("href"))
            prefix=atag.text
            series.append(prefix)

except:
    pass
nav_temp_list=OrderedSet(nav_link)
nav_series_list=OrderedSet(series)
for indexNav,indexSeries in zip(nav_temp_list,nav_series_list):
    # print(indexNav)
    (pageCont, code) = robot.get_content(indexNav, {"method": "get", "bs4": "y"})
    product_banner=pageCont.find("section",{"id":"main-product-banner"})
    # model_name=product_banner.find("div",{"class":"deck-list"}).find_all("li")

    # for modelIndex in model_name:
    #     model_prefx=modelIndex.find("strong").text
    #     model_sufix=modelIndex.find("strong").next_sibling

    # model=model_prefx+" "+model_sufix

    spec_list=[]
    spec_table=pageCont.find("section",{"id":"specifications-sec"}).find_all("div",{"class":"specifications-table"})
    for tableIndex in spec_table:
        try:
            Splist=tableIndex.find("div",{"class":"spacifi-list"}).find_all("li")[1:]
            for spnm in Splist:
                spec_list.append(spnm.text)
        except:
            pass
        model_spec=tableIndex.find_all("div",{"class":"spacifi-list"})[1:]
        for mod in model_spec:
            imges_list = []
            feats_list = []
            option_list = []
            model=indexSeries+" " +mod.find("li").text
            # print(model)

            # print(model_name)
            spcvl=mod.find_all("li")[1:]
            try:
                for specIndex ,specVal_index in zip(spec_list,spcvl):
                    specname=specIndex
                    specvalue=specVal_index.text
                    if re.search(r'(?i)n/a|N/A', specvalue):
                        pass
                    else:
                        if len(specvalue) > 0:
                            if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Torque|Power', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                            elif re.search(r'(?i)Operating|Pressure|Capacity|Fuel|tank|Speed|force', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "operational")
                            elif re.search(r'(?i)Length|Height|Radius|Track|Width|Digging|Range|Size|Thickness', specname):
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
                product_pdf = product_banner.find("ul", {"class": "pro-btn-list"}).find("a").get("href")
                robot.fetch_pdf_manual(product_pdf)
                # print(product_pdf)

            except:
                pass
            try:
                dech4=product_banner.find("h4").text.title()
                feats_list.append(dech4)
            except:
                pass
            try:
                prod_dec = product_banner.find("div", {"class": "pro-discrip"}).find("p").text.title()
                robot.Description(prod_dec.title())
                # print(prod_dec)
            except:
                pass
            try:
                banner_img=product_banner.find_all("img")
                for banrImgIndex in banner_img:
                    imges_list.append(banrImgIndex.get("src"))

            except:
                pass

            try:
                #copfeat_img
                chop_fet_class_img=pageCont.find("section",{"id":"chopper-features-sec"}).find_all("img")
                for IndexCopsclass in chop_fet_class_img:
                    imges_list.append(IndexCopsclass.get("src"))

            except:
                pass
            try:
                #disclamier=
                spec_diclamier=pageCont.find("section",{"id":"specifications-sec"}).find('p').text.title()
                option_list.append(spec_diclamier)
            except:
                pass
            try:
                #chop_fet_text
                chop_fet_class_text=pageCont.find("section",{"id":"chopper-features-sec"})
                try:
                    h3=chop_fet_class_text.find("h3").text.title()
                    feats_list.append(h3)
                except:
                    pass
                try:
                    h4=chop_fet_class_text.find_all("h4")
                    for indexh4 in h4:
                        feats_list.append(indexh4.text.title())

                except:
                    pass
                try:
                    ptag=chop_fet_class_text.find_all("p")[1:]
                    for Indexp in ptag:
                        feats_list.append(Indexp.text.title())
                except:
                    pass


            except:
                pass
            try:
                #subcat
                subcat=product_banner.find("h5").text
                robot.SubCategory(subcat)

            except:
                pass
            try:
                # Wrannty
                section_warrnty=pageCont.find("section",{"id":"pro-warranty-sec"})
                h2=section_warrnty.find("h2").text
                big=section_warrnty.find("big").text
                h3=section_warrnty.find("h3").text
                i=section_warrnty.find("i").text
                wrnty=h2+" "+big+" "+h3+" "+i
                feats_list.append(wrnty)
            except:
                wrnty="warranty 3 Year (Limited) No Hour Limit"
                feats_list.append(wrnty)

            TempFeatList = OrderedSet(feats_list)
            for FetIndex in TempFeatList:
                robot.Features(FetIndex)
            ImgLst = OrderedSet(imges_list)
            for ImgIndex in ImgLst:
                robot.fetch_img_manual(ImgIndex)
            TempOpList = OrderedSet(option_list)
            for OpIndex in TempOpList:
                robot.Options(OpIndex)
            robot.ObjectID(model)
            robot.MasterCategory("Mowers")
            robot.ProductUrl(indexNav)
            robot.Country("US")
            robot.ManufacturerName("Dixie Chopper")
            robot.make_json()
robot.destroy()
