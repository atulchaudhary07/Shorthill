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
URL = "https://www.toyotaforklift.com/lifts"
robot = bot(URL)
driver.get(URL)
time.sleep(5)
product_url_list=[]
pageElement=driver.find_element_by_id("page").find_element_by_class_name("fleet-products").find_elements_by_xpath('//div[@class="product-series col-md-3 col-sm-6 col-xs-12"]')
# print(pageElement.text)
for INdex in pageElement:
    hrf=INdex.find_element_by_tag_name("a").get_attribute("href")
    product_url_list.append(hrf)
orderSet_of_product_urls=OrderedSet(product_url_list)
for urlsIndex in orderSet_of_product_urls:
    try:
        # (soup, code) = robot.get_content(urlsIndex, {"method": "get", "bs4": "y"})
        # robot = bot(URL)
        specList=[]
        Imge_list=[]
        Feat_list=[]
        optnList=[]
        Video_list=[]
        driver.get(urlsIndex)
        time.sleep(3)
        response=driver.page_source
        page_content=BeautifulSoup(response, 'html.parser')
        # spec_table=driver.find_element_by_xpath('//div[@id="specs"]').find_elements_by_xpath('//div[@class="specs-table"]')
        spec_tab=page_content.find("div",{"id":"page"}).find("div",{"id":"specs"}).find("div",{"class":"specs-table"})
        sp_cont=spec_tab.find("table").find("thead").find_all("th")[1:-1]
        for SpIndex in sp_cont:
            specList.append(SpIndex.text)
        models_cont=spec_tab.find("table").find("tbody").find_all("tr")
        for spctab in models_cont:
            model_name=spctab.find_all("td")[0].text
            try:
                #spec
                tds=spctab.find_all("td")[1:]
                for specnm,spval in zip(specList,tds):
                    specname=specnm
                    specvalue=spval.text
                    if re.search(r'(?i)n/a|N/A', specvalue):
                        pass
                    else:
                        if len(specvalue) > 0:
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
                    # printnt("{}:{}".format(specname,specvalue))
            except:
                pass

            try:
                #class="disclaimer"
                disclaimer=spec_tab.find("div",{"class":"disclaimer"}).text
                optnList.append(disclaimer)
            except:
                pass
            try:
                #class="spec-table-note"
                spec_table_note=spec_tab.find("p",{"class":"spec-table-note"}).text
                optnList.append(spec_table_note.strip())
                # print(spec_table_note.strip())
            except:
                pass
            try:
                # SUBCAT
                subcate=spec_tab.find("div",{"class":"spec-table-header clearfix"}).find("h2").text
                robot.SubCategory(subcate.strip())
            except:
                pass
            try:
                # pdf
                pdf=spec_tab.find("a",text="Download Spec Sheet").get("href")
                robot.fetch_pdf_manual(pdf)
            except:
                pass
            try:
                # imges_opt
                optn_img=page_content.find("div",{"id":"options"}).find_all("div",{"class":"top"})
                for optn_img_index in optn_img:
                    imge_opy_styl=optn_img_index.get("style").replace("background-image: url(","").replace(");","").replace('"','')
                    Imge_list.append(imge_opy_styl)

            except:
                pass
            try:
                # option
                option=page_content.find("div",{"id":"options"}).find_all(["p","h3","h2"])
                for optindex in option:
                    optnList.append(optindex.text.strip())
            except:
                pass
            try:
                #videos
                driver.get(urlsIndex)
                time.sleep(3)
                # Vid_class_selenium=driver.find_elements_by_xpath('//div[@class:"responsive-video"]')
                Vid_class_selenium=driver.find_elements_by_tag_name('iframe')
                # Vid_class=page_content.find_all("div",{"class":"responsive-video"})
                for Vid_index in Vid_class_selenium:
                    scr_video=Vid_index.find_element_by_tag_name('iframe').get_attribute("src")
                    if len(scr_video)>3:
                        if re.search(r'(?i)about:blank', scr_video):
                            pass
                        else:
                            Video_list.append(Vid_index.find_element_by_tag_name('iframe').get_attribute("src"))

            except:
                pass
            try:
                # specs-angles
                spec_tab_measure = page_content.find("div",{"id":"page"}).find("div",{"id":"specs"}).find("div",{"class":"specs-angles"})
                try:
                    measure_tab=spec_tab_measure.find_all("div",{"class":"measurement"})
                    for measureIndex in measure_tab:
                        specname=measureIndex.find("h4").text.strip()
                        specvalue=measureIndex.find("p").text.strip()
                        if re.search(r'(?i)n/a|N/A', specvalue):
                            pass
                        else:
                            if len(specvalue) > 0:
                                if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Torque|Power', specname):
                                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                                elif re.search(r'(?i)Operating|Pressure|Capacity|Fuel|tank|Speed|force', specname):
                                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"operational")
                                elif re.search(r'(?i)Length|Height|Radius|Track|Width|Digging|Range', specname):
                                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"dimensions")
                                elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure|Load', specname):
                                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"hydraulics")
                                else:
                                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"operational")
                            else:
                                pass
                        # print(specvalue)
                except:
                    pass
                try:
                    measure_tab_img = spec_tab_measure.find_all("img")
                    for imgIndex in measure_tab_img:
                        src=imgIndex.get("src")
                        Imge_list.append(src)

                        # robot.fetch_img_manual(src)
                except:
                    pass

            except:
                pass

            try:
                #perforamce
                profrmace_tab=page_content.find("div",{"id":"performance"})
                # try:
                #     container=profrmace_tab.find("div",{"class":"content-container"})
                #     # robot.Description(dec)
                # except:
                #     pass
                try:
                    #feature
                    feats=profrmace_tab.find_all("div",{"class":"content-container"})
                    for fetIndex in feats:
                        Tags=fetIndex.find_all(["h2","p","li","section"])
                        for TagIndex in Tags:
                            Feat_list.append(TagIndex.text.strip())
                            # print(TagIndex.text.strip())

                except:
                    pass
                try:
                    #feats_img
                    feats_img = profrmace_tab.find_all("div", {"class":"split-content--grid_image split-content--grid_content"})
                    for feat_img_index in feats_img:
                        styl=feat_img_index.get("style").replace("background-image: url(","").replace(");","").replace('"','')
                        Imge_list.append(styl)

                except:
                    pass
            except:
                pass

            try:
                #overview
                overview=page_content.find("div",{"id":"overview"})
                try:
                    # overview_imge
                    overview_img=overview.find_all("img",{"class":"img-responsive"})
                    for overIndex in overview_img:
                        robot.fetch_img_manual(overIndex.get("src"))

                except:
                    pass

                try:
                #     dec
                    dec=overview.find("div", {"class": "fcp-cd product-content flex-layout--row"}).text.strip()
                    robot.Description(dec)

                except:
                    pass
                try:
                    #feature
                    feats2=overview.find_all("div",{"class":"content-container"})
                    for fetIndex2 in feats2:
                        Tags2=fetIndex2.find_all(["h2","p","li","section"])
                        for TagIndex2 in Tags2:
                            Feat_list.append(TagIndex2.text.strip())
                            # print(TagIndex.text.strip())
                except:
                    pass

            except:
                pass

            ImgLst_lis_order = OrderedSet(Imge_list)
            TempOpList = OrderedSet(optnList)
            TempFeatList = OrderedSet(Feat_list)
            Video_lis_order = OrderedSet(Video_list)
            for Indexof_union in TempFeatList:
                if re.search(r'(?i)GET A SERVICE QUOTE', Indexof_union):
                    pass
                else:
                    robot.Features(Indexof_union)

            for ImgIndex_src in ImgLst_lis_order:
                robot.fetch_img_manual(ImgIndex_src)

            for OpIndex in TempOpList:
                if re.search(r'(?i)Popular Options & Accessories', OpIndex):
                    pass
                else:
                    robot.Options(OpIndex)

            for Vidindex in Video_lis_order:
                robot.fetch_videos(Vidindex)

            robot.ObjectID(model_name)
            robot.MasterCategory("Forklifts")
            robot.ProductUrl(urlsIndex)
            robot.Country("US")
            robot.ManufacturerName("Toyotaforklift")
            robot.make_json()

    except:
        pass
robot.destroy()
driver.close()




