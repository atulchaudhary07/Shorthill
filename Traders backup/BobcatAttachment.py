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

URL = "https://www.bobcat.com/attachments/search-attachments"
path = r'packages/chromedriver'
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=path, options=chrome_options)
# driver.get(URL)
# time.sleep(10)
robot = bot(URL)
(soup,code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
class_hidden=soup.find("div",{"id":"1432287110863"}).find("ul",{"class":"dropdown-menu dtm-subnav-dd-lst"}).find_all("li")[2:]
for li in class_hidden:
    product_link=li.find("a").get("href")
    # print(product_link)
    Subcategory=li.find("a").text
    # print(Subcategory)
    (productPage, code) = robot.get_content(product_link, {"method": "get", "bs4": "y"})
    feats_list = []
    images = []
    Video_tumbnails=[]
    try:
        Fet_child = productPage.find_all("div", {"class": ["col-sm-6 first-child", "col-sm-6 last-child"]})
        for Index_fet_child in Fet_child:

            # print(Index_fet_child)
            try:
                h2 = Index_fet_child.find_all("h2")
                for h in h2:
                    h_text = h.text
                    # print(h_text)
                    feats_list.append(h_text)

            except:
                pass
            try:
                p_tag_child = Index_fet_child.find_all("p")
                for p in p_tag_child:
                    p_text = p.text
                    # print(p_text)
                    feats_list.append(p_text)


            except:
                pass
    except:
        pass

    try:
        tabs = productPage.find("ul", {"class": "list-inline dtm-subnav-tert-lst"}).find_all("a")
        for TabIndex in tabs:
            tab_url=TabIndex.get("href")
            Tab_text=TabIndex.text
            # print(Tab_text)
            driver.get(tab_url)
            # time.sleep(15)
            tab_response = driver.page_source
            tabcont = BeautifulSoup(tab_response, 'html.parser')

            try:
                fet_li= tabcont.find("div", {"id": "content-row"}).find_all("li")
                try:
                    for liTag in fet_li:
                        # print(liTag.text)
                        feats_list.append(liTag.text)
                except:
                    pass

            except:
                pass


            try:
                fet_p = tabcont.find("div", {"id": "content-area"}).find("div", {"class": "ls-cmp-wrap ls-1st"})
                try:
                    p_tag = fet_p.find_all("p")
                    for ptag in p_tag:
                        # print(ptag.text)
                        feats_list.append(ptag.text)
                except:
                    pass

            except:
                pass
            # try:
            #     # fets_page_imges
            #     imges_fet_page = tabcont.find("div", {"id": "content-area"}).find_all("img")
            #     for fetImage_index in imges_fet_page:
            #         images.append(fetImage_index.get("src"))
            #         # print(fetImage_index.get("src"))
            # except:
            #     pass

            try:
                if re.search(r'(?i)Photo|Gallery', Tab_text):
                    driver.get(tab_url)
                    time.sleep(15)
                    try:
                        # driver.implicitly_wait(15)
                        imge_cnt = driver.find_elements_by_xpath("//img[@class='img-responsive media-image']")
                        for image in imge_cnt:
                            src_img = image.get_attribute("src")
                            if src_img is None:
                                pass
                            else:
                                # print(src_img)
                                # robot.fetch_img_manual(src_img)
                                images.append(src_img)
                    except:
                        pass

                    try:
                        video_img=driver.find_elements_by_xpath("//div[@class='video-overlay video-overlay-small']")
                        for video_img_index in video_img:
                            video_img_src=video_img_index.find_element_by_tag_name("img").get_attribute("src")
                            if len(video_img_src) > 0:
                                # print(video_img_src)
                                Video_tumbnails.append(video_img_src)
                            else:
                                pass
                    except:
                        pass
            except:
                pass


    except:
        pass

    try:
        tabs2 = productPage.find("ul", {"class": "list-inline dtm-subnav-tert-lst"}).find_all("a")
        for TabIndex2 in tabs2:
            tab_url2=TabIndex2.get("href")
            Tab_text2=TabIndex2.text
            if re.search(r'(?i)Specifications',Tab_text2):
                driver.get(tab_url2)
                time.sleep(15)
                tab_response2 = driver.page_source
                tabcont2 = BeautifulSoup(tab_response2, 'html.parser')
                model_list = []

                try:

                    product_name = tabcont2.find_all("div", {"class": "ng-binding productName text-condensed text-center"})
                    for modIndex in product_name:
                        product = modIndex.text
                        # print(product)
                        model_list.append(modIndex.text)
                except:
                    pass

                try:
                    counter = 0
                    order_set_of_mod = OrderedSet(model_list)
                    for model_index in range(len(order_set_of_mod) + 1):
                        model = order_set_of_mod[counter]
                        # print(model)
                        subcategory = li.find("a").text
                        option_list = []
                        try:
                            spectables = tabcont2.find("div", {"id": "masterTable"}).find_all("div", {"ng-repeat": "attribute in filterAttributePriority(group.attributes)"})
                            for table in spectables:
                                specname = table.find("div", {"class": "td text-condensed ng-binding"}).text
                                specvalue = table.find_all("div", {"class": "td text-center ng-scope"})[counter].text
                                # print(specname)
                                # print(specvalue)
                                if re.search(r'(?i)n/a|N/A', specvalue):
                                    pass
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
                        try:  # compatiblity
                            # listof_compc=spec_Tab_soup.find("div", {"id": "masterTable"}).find_all("")
                            tables = tabcont2.find("div", {"id": "masterTable"}).find("div", {"ng-if": "accordion['compatibleProducts']"}).find_all("div", {"ng-repeat": "compatibleProductCategory in compatibleProductsByCategory[compatibilityTarget]"})
                            for table_index in tables:
                                Compac_table = table_index.find_all("div", {"class": "tr even ng-scope"})
                                for compac_index in Compac_table:
                                    # compac_model_name = compac_index.find("div", {"class": "td text-condensed"}).text
                                    try:
                                        Stand_img = compac_index.find_all("div", {"class": "td text-center ng-scope"})[counter].find("span", {"class": "standardImage ng-scope"}).get("class")
                                        if len(Stand_img) > 0:
                                            compac_model_name = compac_index.find("div", {"class": "td text-condensed"}).text
                                            # print(compac_model_name)
                                            option_list.append(compac_model_name)
                                    except:
                                        pass
                        except:
                            pass
                        dec = "Bobcat" + " " + model
                        robot.Description(dec)
                        # ImgLst = OrderedSet(images)
                        ImgLst = OrderedSet(OrderedSet(images).difference(OrderedSet(Video_tumbnails)))
                        try:
                            if len(ImgLst)>0:
                                for ImgIndex in ImgLst:
                                    robot.fetch_img_manual(ImgIndex)
                                    # print(ImgIndex)
                            else:
                                overview = productPage.find("div",{"id": "content-area"}).find("section",{"class":"container flexible-content"}).find("img").get("src")
                                robot.fetch_img_manual(overview)
                                # print(overview)

                                # print("https://cdn.cwsplatform.com/assets/no-photo-available.png")
                                # robot.fetch_img_manual("https://cdn.cwsplatform.com/assets/no-photo-available.png")
                        except:
                            pass
                        TempFeatList = OrderedSet(feats_list)
                        for FetIndex in TempFeatList:
                            if FetIndex=="Photos" or FetIndex=="Videos":
                                pass
                            else:
                                robot.Features(FetIndex)
                        TempOpList = OrderedSet(option_list)
                        for OpIndex in TempOpList:
                            robot.Options(OpIndex)
                        robot.ObjectID(model)
                        robot.SubCategory(subcategory)
                        robot.MasterCategory("Attachments & Implements")
                        robot.ProductUrl(tab_url2)
                        robot.Country("US")
                        robot.ManufacturerName("Bobcat")
                        robot.make_json()
                        counter = counter + 1

                except:
                    pass
    except:
        pass

robot.destroy()
driver.close()

