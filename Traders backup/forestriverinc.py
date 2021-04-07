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
URL = "https://forestriverinc.com/rvs/"
driver.get(URL)
robot = bot(URL)
# driver.implicitly_wait(5)
url_list=[]
Cat_list=[]

subcat=driver.find_element_by_id("RVs").find_element_by_class_name("common-padding").find_elements_by_tag_name("a")
for Index in subcat:
    if Index is not None:
        sucat_URL=Index.get_attribute("href")
        Categ = Index.text
        Cat_list.append(Categ)
        if len(sucat_URL)>2:
            url_list.append(Index.get_attribute("href"))
        # print(sucat_URL)


UniqURL_list=OrderedSet(url_list)
for url,cat in zip(UniqURL_list,Cat_list):
    # Categ="RVS
    Option = []
    Feats = []
    pdf_attach=[]
    EXt_img = []
    (soup, code) = robot.get_content(url, {"method": "get", "bs4": "y"})
    # print(soup)
    try:
        try:
            fets_op = soup.find("div", {"id": "features"}).find_all("div", {"class": "card float-left feature-item"})
            for FetIndex in fets_op:
                header = FetIndex.find("div", {"class": "card-header"}).text
                if re.search(r'(?i)OPTIONS|option', header):
                    opts = FetIndex.find("div", {"class": "card-body"}).find_all("li")
                    for OpIndex in opts:
                        Option.append(OpIndex.text.strip())
                else:
                    Feats.append(header)
                    # print(header)
                    fets = FetIndex.find("div", {"class": "card-body"}).find_all("li")
                    for fetIndex in fets:
                        # print(fetIndex.text.str)
                        Feats.append(fetIndex.text.strip())
        except:
            pass
        try:
            # pdf
            attchemnt = soup.find("div", {"id": "literature"}).find_all("a", {"class": "text-frdark"})
            for attchemnt_index in attchemnt:
                pdf_attach.append(attchemnt_index.get("href").replace("//",""))
        except:
            pass
        try:#exter Images
            ExtImges=soup.find("div",{"id":"gallery"}).find("div",{"id":"product-gallery"}).find_all("img")
            for ExtImgIndex in ExtImges:
                extr_src="https://forestriverinc.com/rvs"+ExtImgIndex.get("src")
                EXt_img.append(extr_src)

        except:
            pass

        product_url=soup.find("div",{"id":"floorplans"}).find_all("div",{"class":"float-left floorplan bg-white"})
        for product_url_index in product_url:
            product_href="https://forestriverinc.com/rvs/"+product_url_index.find("a",{"class":"text-frdark block"}).get("href").replace(" ","")
            (prodsoup, code) = robot.get_content(product_href, {"method": "get", "bs4": "y"})
            imges = []
            # videos = []
            modelName=product_url_index.find("h3").text
            # print(modelName)
            try:
                dec=prodsoup.find("div",{"id":"ContentPlaceHolder1_panDescription"}).text.strip()
                if len(dec)>3:
                    # print(dec)
                    robot.Description(dec)
                else:
                    dec = "Forest River" + " " + modelName
                    # print(dec)
                    robot.Description(dec)
            except:
                pass
                # dec="Forest River"+" "+modelName
                # robot.Description(dec)
            try:
                subcatName=prodsoup.find("div",{"class":"clear-fix text-large"}).text.strip()
                if re.search(r'(?i)Temporarily Unavailable', subcatName):
                    robot.SubCategory("Trailers")
                else:
                    robot.SubCategory(subcatName)

            except:
                pass
            try:
                floor_plan_imge="https://forestriverinc.com/"+prodsoup.find("a",{"class":"text-medium text-dosis floorplan-image"}).get("href")
                robot.fetch_img_manual(floor_plan_imge)
            except:
                pass
            try:
                imge=prodsoup.find("div",{"id":"ContentPlaceHolder1_divModelGallery"}).find_all("img")
                for imgindex in imge:
                    imges.append("https://forestriverinc.com/"+imgindex.get("src"))
            except:
                pass
            try:
                spc_list=[]
                spec2list=[]
                specs=prodsoup.find("div",{"id":"m-specifications"}).find("div",{"class":"model-specs w-100"}).find_all("strong")
                for spIndx in specs:
                    spname=spIndx.text.strip()
                    spc_list.append(spname)
                    # print(spname)

                try:
                    specs2 = prodsoup.find("div",{"id": "m-specifications"}).find("div", {"class": "model-specs w-100"}).find_all("div")
                    for Index2 in specs2:
                        if len(Index2.text) is not None:
                            if Index2.text in spc_list:
                                pass
                            else:
                                spec2list.append(Index2.text.strip())
                except:
                    pass
                unique_list=[]
                for Item_spclist in spec2list:
                    # for item_index in spc_list:
                    if Item_spclist in spc_list:
                        # print("Pass")
                        pass
                    else:
                        unique_list.append(Item_spclist)

                # Spname_list=OrderedSet(spc_list)
                # speValueList = spec2list.difference(OrderedSet(spc_list))
                # speValueList = spec2list.remove(spc_list)
                # print(spec2list)

                for name,value in zip(spc_list,unique_list):
                    specname=name
                    # print(specname)
                    specvalue=value
                    # print(" {} :  {} ".format(specname,specvalue))
                    # print(specvalue)
                    if len(specvalue) > 0:
                        if re.search(r'(?i)N/A|n/a', specvalue):
                            pass
                        else:

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
                #360_imge
                img_360=prodsoup.find("",{"id":"ContentPlaceHolder1_divModel360"}).find("a",{"class":"position-relative"}).get("href")
                robot.fetch_videos(img_360)

            except:
                pass

            # try:
            #     #spec_defination
            #     spec_def=prodsoup.find("div",{"id":"ContentPlaceHolder1_panTowableSpecDefinitions"}).find_all("p")
            #     for spec_defIndex in spec_def:
            #         spec_def_text=spec_defIndex.text.strip()
            #         Feats.append(spec_def_text)
            #
            # except:
            #     pass

            try:
                #video
                driver.get(product_href)
                vid_src=driver.find_element_by_id("model-video").find_element_by_tag_name("iframe").get_attribute("src")
                # video_src=prodsoup.find("div",{"id":"ContentPlaceHolder1_divModelVideo"}).find("iframe")
                robot.fetch_videos(vid_src)
            except:
                pass

            ExtImges=OrderedSet(EXt_img)
            for Index_extImges in ExtImges:
                robot.fetch_img_manual(Index_extImges)
            ImgLst_lis_order = OrderedSet(imges)
            for ImgIndex_src in ImgLst_lis_order:
                robot.fetch_img_manual(ImgIndex_src)

            TempOpList = OrderedSet(Option)
            for OpIndex in TempOpList:
                robot.Options(OpIndex)

            TempFeatList = OrderedSet(Feats)
            for Indexof_TempFeatList in TempFeatList:
                robot.Features(Indexof_TempFeatList)
            tempPDF=OrderedSet(pdf_attach)
            for pdfs in tempPDF:
                robot.fetch_pdf_manual(pdfs)



            robot.ObjectID(modelName)
            robot.MasterCategory("Travel Trailers")
            # robot.SubCategory(subcatName)
            robot.ProductUrl(product_href)
            robot.Country("US")
            robot.ManufacturerName("Forest River")
            robot.make_json()
    except:
        pass
        # try:
        #     product_url2 = soup.find("div", {"id": "ContentPlaceHolder1_panFamily"}).find_all("div",{"class": "float-left floorplan bg-white"})
        #     for product_url_index2 in product_url2:
        #         product_href2 = "https://forestriverinc.com" + product_url_index2.find("a", {"class": "text-frdark"}).get("href").replace(" ", "")
        #         (soup2, code) = robot.get_content(product_href2, {"method": "get", "bs4": "y"})
        #         try:
        #             fets_op = soup2.find("div", {"id": "features"}).find_all("div", {"class": "card float-left feature-item"})
        #             for FetIndex in fets_op:
        #                 header = FetIndex.find("div", {"class": "card-header"}).text
        #                 if re.search(r'(?i)OPTIONS|option', header):
        #                     opts = FetIndex.find("div", {"class": "card-body"}).find_all("li")
        #                     for OpIndex in opts:
        #                         Option.append(OpIndex.text.strip())
        #                 else:
        #                     Feats.append(header)
        #                     # print(header)
        #                     fets = FetIndex.find("div", {"class": "card-body"}).find_all("li")
        #                     for fetIndex in fets:
        #                         # print(fetIndex.text.str)
        #                         Feats.append(fetIndex.text.strip())
        #         except:
        #             pass
        #         try:
        #             # pdf
        #             attchemnt = soup2.find("div", {"id": "literature"}).find_all("a", {"class": "text-frdark"})
        #             for attchemnt_index in attchemnt:
        #                 robot.fetch_pdf_manual(attchemnt_index.get("href"))
        #         except:
        #             pass
        #
        #         product_url = soup2.find("div", {"id": "floorplans"}).find_all("div",{"class": "float-left floorplan bg-white"})
        #         for product_url_index in product_url:
        #             product_href = "https://forestriverinc.com/rvs/" + product_url_index.find("a",{"class": "text-frdark block"}).get("href").replace(" ", "")
        #             (prodsoup, code) = robot.get_content(product_href, {"method": "get", "bs4": "y"})
        #             modelName = product_url_index.find("h3").text
        #             print(modelName)
        #             try:
        #                 dec=prodsoup.find("div",{"id":"ContentPlaceHolder1_panDescription"}).text.strip()
        #                 if len(dec)>2:
        #                     robot.Description(dec)
        #             except:
        #                 dec="Forest River"+" "+modelName
        #                 robot.Description(dec)
        #             try:
        #                 subcatName=prodsoup.find("div",{"class":"clear-fix text-large"}).text.strip()
        #                 robot.SubCategory(subcatName)
        #             except:
        #                 pass
        #             try:
        #                 floor_plan_imge="https://forestriverinc.com/"+prodsoup.find("a",{"class":"text-medium text-dosis floorplan-image"}).get("href")
        #                 robot.fetch_img_manual(floor_plan_imge)
        #             except:
        #                 pass
        #             try:
        #                 imge=prodsoup.find("div",{"id":"ContentPlaceHolder1_divModelGallery"}).find_all("img")
        #                 for imgindex in imge:
        #                     imges.append("https://forestriverinc.com/"+imgindex.get("src"))
        #             except:
        #                 pass
        #             try:
        #                 spc_list=[]
        #                 spec2list=[]
        #                 specs=prodsoup.find("div",{"id":"m-specifications"}).find("div",{"class":"model-specs w-100"}).find_all("strong")
        #                 for spIndx in specs:
        #                     spname=spIndx.text.strip()
        #                     spc_list.append(spname)
        #
        #                 try:
        #                     specs2 = prodsoup.find("div",{"id": "m-specifications"}).find("div", {"class": "model-specs w-100"}).find_all("div")
        #                     for Index2 in specs2:
        #                         if len(Index2.text)>1:
        #                             spec2list.append(Index2.text.strip())
        #                 except:
        #                     pass
        #                 speValueList = OrderedSet(spec2list).difference(OrderedSet(spc_list))
        #
        #                 for name,value in zip(spc_list,speValueList):
        #                     specname=name
        #                     specvalue=value
        #                     # print(specname)
        #                     # print(specvalue)
        #                     if len(specvalue) > 0:
        #                         if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Torque|Power', specname):
        #                             robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
        #                         elif re.search(r'(?i)Operating|Pressure|Capacity|Fuel|tank|Speed|force', specname):
        #                             robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "operational")
        #                         elif re.search(r'(?i)Length|Height|Radius|Track|Width|Digging|Range', specname):
        #                             robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "dimensions")
        #                         elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure|Load', specname):
        #                             robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "hydraulics")
        #                         else:
        #                             robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "operational")
        #                     else:
        #                         pass
        #
        #
        #             except:
        #                 pass
        #             try:
        #                 #360_imge
        #                 img_360=prodsoup.find("",{"id":"ContentPlaceHolder1_divModel360"}).find("a",{"class":"position-relative"}).get("href")
        #                 robot.fetch_videos(img_360)
        #
        #             except:
        #                 pass
        #
        #             try:
        #                 #spec_defination
        #                 spec_def=prodsoup.find("div",{"id":"ContentPlaceHolder1_panTowableSpecDefinitions"}).find_all("p")
        #                 for spec_defIndex in spec_def:
        #                     spec_def_text=spec_defIndex.text.strip()
        #                     Feats.append(spec_def_text)
        #
        #             except:
        #                 pass
        #
        #             try:
        #                 #video
        #                 driver.get(product_href)
        #                 vid_src=driver.find_element_by_id("model-video").find_element_by_tag_name("iframe").get_attribute("src")
        #                 # video_src=prodsoup.find("div",{"id":"ContentPlaceHolder1_divModelVideo"}).find("iframe")
        #                 robot.fetch_videos(vid_src)
        #             except:
        #                 pass
        #
        #             ImgLst_lis_order = OrderedSet(imges)
        #             for ImgIndex_src in ImgLst_lis_order:
        #                 robot.fetch_img_manual(ImgIndex_src)
        #
        #             TempOpList = OrderedSet(Option)
        #             for OpIndex in TempOpList:
        #                 robot.Options(OpIndex)
        #
        #             TempFeatList = OrderedSet(Feats)
        #             for Indexof_TempFeatList in TempFeatList:
        #                 robot.Features(Indexof_TempFeatList)
        #
        #             robot.ObjectID(modelName)
        #             robot.MasterCategory(cat)
        #             # robot.SubCategory(subcatName)
        #             robot.ProductUrl(product_href)
        #             robot.Country("US")
        #             robot.ManufacturerName("Forest River")
        #             robot.make_json()


        # except:
        #     pass




driver.close()
robot.destroy()


