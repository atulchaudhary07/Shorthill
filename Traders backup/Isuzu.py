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
URL = "https://www.isuzucv.com"
robot = bot(URL)
(soup, code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
navgation_link=soup.find("ul",{"id":"main-menu"}).find("li").find("ul").find_all("li")[:-2]
for NavIndex in navgation_link:
    product_url=URL+NavIndex.find("a").get("href")
    # Subcategory=NavIndex.find("a").text
    (prodcontent, code) = robot.get_content(product_url, {"method": "get", "bs4": "y"})
    main_section=prodcontent.find("section",{"id":"main"})
    Images=[]
    Videos=[]
    feats=[]
    options=[]
    # Feat_list_2=[]
    decp=[]
    modeltemp = []
    # model_lis=[]
    try:
        #Images
        # img=main_section.find_all("img")
        for indexImg in main_section.find_all("img"):
            src_img=indexImg.get("src")
            if re.search(r'(?i)https:',src_img):
                imgSrc=src_img
                Images.append(imgSrc)
            else:
                imgSrc=URL+src_img
                Images.append(imgSrc)
    except:
        pass

    try:
        # color
        color=main_section.find("div",{"id":"colors"}).find_all("li")
        for colorIndex in color:
            color_name=colorIndex.find("img").get("alt")
            options.append(color_name)

    except:
        pass

    try:
        #fet2
        fets_in_span=main_section.find_all("span",{"class":"centered_text"})
        for fet2index in fets_in_span:
            feats.append(fet2index.text.strip())
    except:
        pass
    try:
        #videos
        for Vid in main_section.find_all("iframe"):
            Vid_src=Vid.get("src")
            Videos.append(Vid_src)
        # vid=main_section.find_all("iframe")
    except:
        pass

    try:#feature
        for fet_index in main_section.find_all("p")[1:]:
            pTag_text=fet_index.text.strip()
            if re.search(r'(?i)FIND A DEALER|6.0L Model Shown|Available color', pTag_text):
                pass
            else:
                feats.append(pTag_text)
    except:
        pass

    try:
        # model

        model=main_section.find("div",{"class":"jcarousel_wrap"}).find_all("li")
        for ModelIndex in model:
            model_name=ModelIndex.find("h5").text
            modeltemp.append(model_name)

    except:
        pass
    try:
        # Warrnty
        Warrenty=main_section.find("div",{"id":"warranty"}).find_all("li")
        # print(Warrenty)
        for wrntyIndex in Warrenty:
            Wrnty_Text=wrntyIndex.text.title().strip()
            feats.append(Wrnty_Text)
    except:
        pass

    try:
        # Warrenty_doc
        Warrenty_pdf=URL+main_section.find("a",text="Download Warranty").get("href")
        robot.fetch_pdf_manual(Warrenty_pdf)
    except:
        pass
    try:
        tempmods = OrderedSet(modeltemp)
        # for modelIndex in tempmods:
        model_cont = main_section.find("div", {"class": "jcarousel_wrap"}).find_all("li")
        for modelIndex,liIndex in zip(tempmods,model_cont):
            # model_name=liIndex.find("h5").text
            # modeltemp.append(model_name)
            subcat = NavIndex.find("a").text
            robot.SubCategory(subcat)
            # print(Subcategory)

            product_img = URL + liIndex.find("img").get("src")
            robot.fetch_img_manual(product_img)

            try:  # spec
                specs = liIndex.find_all("b")
                for spIndex in specs:
                    specname = spIndex.text.strip()
                    specvalue = spIndex.next_sibling.strip().replace("lbs.","lbs")
                    if re.search(r'(?i)n/a|N/A', specvalue):
                        pass

                    else:
                        if len(specvalue) > 0:
                            if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Torque|Power', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                            elif re.search(r'(?i)Length|Height|Radius|Track|Width|Digging|Range', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"dimensions")
                            elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure|Load', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"hydraulics")
                            else:
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"operational")
                        else:
                            pass
            except:
                pass

            try:
                # pdf
                PDF = liIndex.find_all("a")
                for pdfindex in PDF:
                    pdfSrc = URL + pdfindex.get("href")
                    robot.fetch_pdf_manual(pdfSrc)
            except:
                pass

            try:
                dec = main_section.find_all("div", {"class": ["bottom_text bottom_text_no_background", "gray_text gray_text_smaller"]})
                for DecIndex in dec:
                    decp.append(DecIndex.text.strip())
                # robot.Description(dec)
            except:
                pass

            ImgLst_lis_order = OrderedSet(Images).difference(OrderedSet(product_img))
            for ImgIndex_src in ImgLst_lis_order:
                robot.fetch_img_manual(ImgIndex_src)

            TempFeatList = OrderedSet(feats)
            for Indexof_union in TempFeatList:
                title_case_fets=Indexof_union.title()
                if re.search(r'(?i)Available Colors|See your authorized Isuzu dealer for warranty details|See your authorized Isuzu dealer for extended warranty details', title_case_fets):
                    pass
                else:
                    robot.Features(title_case_fets)

            tempVid = OrderedSet(Videos)
            for IndexofVid in tempVid:
                robot.fetch_videos(IndexofVid)
            tempoptions = OrderedSet(options)
            for OpIndex in tempoptions:
                robot.Options(OpIndex)
            tempdec=OrderedSet(decp)
            descp="".join(tempdec)
            robot.ObjectID(modelIndex)
            robot.Description(descp)
            robot.MasterCategory("Trucks")
            robot.ProductUrl(product_url)
            robot.Country("US")
            robot.ManufacturerName("Isuzu Trucks")
            robot.make_json()
    except:
        pass
robot.destroy()
