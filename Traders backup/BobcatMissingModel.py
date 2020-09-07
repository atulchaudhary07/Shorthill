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

URL = "https://www.bobcat.com/index"
path = r'packages/chromedriver'
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=path, options=chrome_options)
# driver.get(URL)
# time.sleep(10)
robot = bot(URL)
(soup,code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
class_nav=soup.find("ul",{"id":"main-nav"}).find_all("li",{"data-nav-type":["Product Family","Product Group"]})[3:]
for navIndex in class_nav:
    h4=navIndex.find_all("h4")
    for h4Index in h4:
        product_link=h4Index.find("a").get("href")
        # subcat=h4Index.find("a").text
        # print(subcat)
        (productPage,code) = robot.get_content(product_link, {"method": "get", "bs4": "y"})
        feats_list = []
        images = []
        option_list = []
        Video_tumbnails=[]
        try:
            dec = productPage.find("section", {"class": "container flexible-content"}).find("p").text
            # print(dec)
            robot.Description(dec)
        except:
            pass
        try:
            msrp = product_img = productPage.find("section",{"class": ["free-text container", "container flexible-content", ]}).find("h4").text
            robot.Msrp(msrp)
            # print(msrp)

        except:
            pass

        try:
            featgrouping = productPage.find("div", {"id": "productGrouping"})
            featHeading = featgrouping.find_all("h3", {"class": "panel-title"})
            feat_cont = featgrouping.find_all("div", {"class": "panel-body"})
            for head, cont in zip(featHeading, feat_cont):
                feature = head.text + ": " + cont.text
                feats_list.append(feature)
                # print(feature)
        except:
            pass
        try:
            container_feats = productPage.find("div", {"id": "productGrouping"}).find_all("a",{"class": "lightbox product-details lbox-trigger border-grey"})
            for hidden_Md in container_feats:
                feats_list.append(hidden_Md.text.title())

        except:
            pass

        try:
            tabs = productPage.find("ul", {"class": "list-inline dtm-subnav-tert-lst"}).find_all("a")
            for TabIndex in tabs:
                tab_url = TabIndex.get("href")
                driver.get(tab_url)
                # time.sleep(15)
                tab_response = driver.page_source
                tabcont = BeautifulSoup(tab_response, 'html.parser')
                try:

                    driver.get(tab_url)
                    time.sleep(10)

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
                        video_img = driver.find_elements_by_xpath("//div[@class='video-overlay video-overlay-small']")
                        for video_img_index in video_img:
                            video_img_src = video_img_index.find_element_by_tag_name("img").get_attribute("src")
                            if len(video_img_src)>0:
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
                tab_url2 = TabIndex2.get("href")
                driver.get(tab_url2)
                time.sleep(15)
                tab_response2 = driver.page_source
                tabcont2 = BeautifulSoup(tab_response2, 'html.parser')
                model_list = []

                try:
                    product_name = tabcont2.find_all("div",{"class": "ng-binding productName text-condensed text-center"})
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
                        Model_Id=model.replace("Bobcat","").strip()
                        subcategory=h4Index.find("a").text
                        subcat = subcategory.replace(model,"").strip()
                        # print(Model_Id)
                        # print(subcat)
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
                                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"engine")
                                        elif re.search(r'(?i)Operating|Pressure|Capacity|Fuel|tank|Speed',specname):
                                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"operational")
                                        elif re.search(r'(?i)Length|Height||Radius|Track|Width|Load', specname):
                                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"dimensions")
                                        elif re.search(r'(?i)Weight|Load', specname):
                                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"weights")
                                        elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure', specname):
                                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"hydraulics")
                                        else:
                                            robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"other")
                                    else:
                                        pass
                        except:
                            pass
                        try:
                            # feature and option

                            Fet_opt_data = tabcont2.find("div", {"id": "masterTable"}).find_all("div", {"class": ["tr ng-scope specRow even", "tr ng-scope specRow odd"]})

                            for data in Fet_opt_data:
                                try:
                                    option_class = data.find("div", {"class": "optionalImage"}).get("class")
                                    if option_class is not None:
                                        option_data = data.find("div", {"td text-condensed ng-binding"}).text
                                        option_list.append(option_data.title())
                                        # print("option_class")
                                except:
                                    pass
                                try:
                                    feat_class = data.find("div", {"class": "standardImage"}).get("class")
                                    if feat_class is not None:
                                        feature_data = data.find("div", {"td text-condensed ng-binding"}).text
                                        # print(feature_data)
                                        feats_list.append(feature_data.title())

                                except:
                                    pass

                        except:
                            pass

                        # ImgLst = OrderedSet(images)
                        ImgLst = OrderedSet(OrderedSet(images).difference(OrderedSet(Video_tumbnails)))

                        try:
                            if len(ImgLst) >= 1:
                                for ImgIndex in ImgLst:
                                    robot.fetch_img_manual(ImgIndex)
                                    # print("Available")
                            else:
                                # print("https://cdn.cwsplatform.com/assets/no-photo-available.png")
                                robot.fetch_img_manual("https://cdn.cwsplatform.com/assets/no-photo-available.png")
                        except:
                            pass

                        TempFeatList = OrderedSet(feats_list).difference(OrderedSet(option_list))
                        for FetIndex in TempFeatList:
                            robot.Features(FetIndex)
                        TempOpList = OrderedSet(option_list)
                        for OpIndex in TempOpList:
                            robot.Options(OpIndex)

                        if re.search(r'(?i)Loaders|Compact Track Loader|kid-Steer Loader|All-Wheel Steer Loader|Small Articulated Loader|Mini Track Loader',subcat):
                            robot.MasterCategory("Loaders")
                        elif re.search(r'(?i)Excavators|Compact Excavator|Large Excavator', subcat):
                            robot.MasterCategory("Excavators")
                        elif re.search(r'(?i)Tractors|Compact Tractor|Sub-Compact Tractor', subcat):
                            robot.MasterCategory("Tractors")
                        elif re.search(r'(?i)Utility Products|Utility Vehicles|Diesel Utility Vehicle|Gas Utility Vehicle|Toolcat',subcat):
                            robot.MasterCategory("Utility Vehicles")
                        else:
                            robot.MasterCategory("Telehandlers")

                        robot.ObjectID(Model_Id)
                        robot.SubCategory(subcat)
                        robot.ProductUrl(product_link)
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


