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
main_url="https://www.rightline.com"
URL = "https://www.rightline.com/attachments/"
robot = bot(URL)
(soup, code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
class_main=soup.find("div",{"role":"main"}).find_all("section",{"class":"pt-5 pb-10"})
for classMainIndex in class_main:
    subcat_link= main_url+classMainIndex.find("a").get("href")
    cat_name=classMainIndex.find("h1").text.title().strip()
    # print(cat_name)
    driver.get(subcat_link)
    driver.implicitly_wait(5)
    page_response=driver.page_source
    sbcat_page_soup=BeautifulSoup(page_response,'html.parser')
    # (sbcat_page_soup, code) = robot.get_content(subcat_link, {"method": "get", "bs4": "y"})
    spec_tabs=sbcat_page_soup.find("div",{"id":"specification-table"}).find_all("div",{"class":"product-table"})
    for spectable in spec_tabs:
        model_names_tab=spectable.find_all("table")
        for table in model_names_tab:
            specname_list = []
            th = table.find("thead").find("tr").find_all("th")[1:]
            for th_index in th:
                specname_list.append(th_index.text)
            tablebody = table.find("tbody").find_all("tr")
            for tds in tablebody:
                model = tds.find("td").text
                Sub_heading = spectable.find("h4").text.strip().replace(" | ","|")
                td_text=tds.find_all("td")[1:]
                cat_name = classMainIndex.find("h1").text.strip()
                subcat = sbcat_page_soup.find("section", {"class": "texty-10 mb-20"}).find("h1").text.title().strip()
                full_product=model+" "+Sub_heading
                feat_list=[]
                Images_list=[]
                Options_list=[]

                OrderSpecList=OrderedSet(specname_list)
                for SpecNm, SpecVal in zip(OrderSpecList,td_text ):
                    specname = SpecNm.title()
                    specvalue = SpecVal.text
                    if re.search(r'(?i)n/a|N/A|login',specvalue):
                        pass
                    else:
                        if len(specvalue) > 2:
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
                try:
                    #description
                    dec=sbcat_page_soup.find("h3",{"class":"text-secondary-gray"}).text.strip()
                    robot.Description(dec)

                except:
                    pass
                try:
                    #features
                    fet_section=sbcat_page_soup.find("section",{"id":"feature"}).find_all("div",{"class":"texty-3 mb-20"})
                    try:
                        for ft in fet_section:
                            try:
                            #heading
                                Heading=ft.find("h1").text.strip()
                                feat_list.append(Heading)
                            except:pass
                            try:
                                #ptag
                                ptag=ft.find_all("p")
                                for ptext in ptag:
                                    feat_list.append(ptext.text)
                            except:pass
                            try:
                                #li
                                li=ft.find_all("li")
                                for liIndex in li:
                                    feat_list.append(liIndex.text)

                            except:pass


                    except:
                        pass

                except:
                    pass

                try:
                    #Images
                    picture_class=sbcat_page_soup.find_all("picture")
                    for picture_index in picture_class:
                        img_src=picture_index.find("img").get("srcset")
                        Images_list.append(img_src)

                except:
                    pass

                try:
                    #option
                    op=sbcat_page_soup.find("section",{"class":"text-container text-container-1080px"})
                    try:
                        #option_h3_heading_in_white
                        op_h3_class=op.find_all("h3")
                        for Op_h3_index in op_h3_class:
                            Options_list.append(Op_h3_index.text)

                    except:
                        pass

                    try:
                        #option_container_text
                        option_p_tag=op.find_all("p")
                        for Op_p_index in option_p_tag:
                            Options_list.append(Op_p_index.text)

                    except:
                        pass

                except:
                    pass

                ImgLst=OrderedSet(Images_list)
                for ImgIndex in ImgLst:
                    new_src_img_link=ImgIndex.split("?date")[0]
                    # if re.search(r'(?i).jpg', ImgIndex):
                    robot.fetch_img_manual(new_src_img_link)
                TempFeatList=OrderedSet(feat_list)
                for FetIndex in TempFeatList:
                    robot.Features(FetIndex)
                TempOpList=OrderedSet(Options_list)
                for OpIndex in TempOpList:
                    robot.Options(OpIndex)

                robot.ObjectID(full_product)
                robot.MasterCategory(cat_name)
                robot.SubCategory(subcat)
                robot.ProductUrl(subcat_link)
                robot.Country("US")
                robot.ManufacturerName("Rightline")
                robot.make_json()

robot.destroy()
driver.close()















