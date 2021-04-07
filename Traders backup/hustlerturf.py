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
URL = "https://www.hustlerturf.com"
robot = bot(URL)
(soup,code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
subnav=soup.find("div",{"class":"topnav-bar-2"}).find_all("div",{"class":"topnav-bar-2-dropdown w-dropdown"})
product_url_list=["https://www.hustlerturf.com/products/mdv-levelift","https://www.hustlerturf.com/products/mdv"]
for navIndex in subnav:
    nav=navIndex.find("nav",{"class":"topnav-bar-2-dropdown-list w-dropdown-list"}).find_all("a")
    for Nav_link in nav:
        src=Nav_link.get("href")
        if re.search(r'(?i)https://', src):
            # print(src)
            pass
        else:
            src_Url=URL+src
            # print(src_Url)
            try:
                #models_from_same_structure
                (soup2,code) = robot.get_content(src_Url, {"method": "get", "bs4": "y"})
                product_links=soup2.find("div",{"class":"max-width"}).find_all("div",{"role":"listitem"})
                for prod_nav in product_links:
                    a_tag=prod_nav.find_all("a")
                    for index_a in a_tag:
                        if re.search(r'(?i)#|promotions|compare|https://www.hustlerturf.com/financing', index_a.get("href")):
                            pass
                        else:
                            urls=URL+index_a.get("href")
                            product_url_list.append(urls)
                                # print(urls)
            except:
                # print("fail")
                pass

for productIndx in product_url_list:
    feats=[]
    images=[]
    Pdfs_file=[]
    (ProdPageSoup, code) = robot.get_content(productIndx, {"method": "get", "bs4": "y"})

    try:
        #hidden_setion_h3_tag
        hidden_section=ProdPageSoup.find("div",{"class":"max-width"}).find_all("h3",{"class":"h6 _0-top-margin"})
        for h3Index in hidden_section:
            if len(h3Index.text)>3:
                feats.append(h3Index.text)
        # robot.Description(dec)
    except:
        pass
    try:
        #hidden_setion_p_tag
        hidden_section_2=ProdPageSoup.find("div",{"class":"max-width"}).find_all("p",{"class":"text-slate"})
        for pIndex in hidden_section_2:
            if len(pIndex.text)>3:
                feats.append(pIndex.text)
                # feats.append(pIndex.text)
        # robot.Description(dec)
    except:
        pass
    try:
        #feature_under_card
        fets1 = ProdPageSoup.find("div",{"class":"product-hero-right-card"}).find("ul",{"role":"list"}).find_all("li")
        for fet1index in fets1:
            feats.append(fet1index.text)
    except:
        pass

    # try:
    #     Msrp=ProdPageSoup.find("div",{"class":"product-hero-right-card"}).find("div",{"class":"product-price-wrapper"}).find("div",{"class":"h6 text-space-5"})
    #     robot.Msrp(Msrp.text)
    # except:
    #     pass

    try:
        images_in_card=ProdPageSoup.find("div",{"class":"product-images-tabs"}).find_all("img")
        for ImgIndex in images_in_card:
            imgSrc=ImgIndex.get("src")
            images.append(imgSrc)
    except:
        pass
    try:
        #feats2_text_content
        Fets2=ProdPageSoup.find("div",{"id":"Features"}).find_all("div",{"class":"card-content"})
        for IndexFet2 in Fets2:
            Fetoncate=IndexFet2.find("h3").text+" "+ IndexFet2.find("p").text
            feats.append(Fetoncate)
    except:
        pass
    try:
        # feats2_Imge
        Fets2_imhg = ProdPageSoup.find("div", {"id": "Features"}).find_all("div", {"class": "card-image-wrapper"})
        for IndexFet2_img in Fets2_imhg:
            images.append(IndexFet2_img.find("img").get("src"))

    except:
        pass

    try:
        #pdf
        pdf_content=ProdPageSoup.find("a",text="Download specs PDF").get("href")
        Pdfs_file.append(pdf_content)
    except:
        pass



    try:
        # Spec
        # spec = ProdPageSoup.find("div", {"id": "Specs"}).find("div", {"class": "specs-table-full-width"})
        # print(spec.text)
        # print(spec)
        # spec_header_list=[]
        # counter=0
        spec = ProdPageSoup.find("div",{"id":"Specs"}).find("div",{"class":"specs-table-full-width"}).find_all("div",{"class":"specs-table-wrapper"})
        for IndexSpec in spec:
            full_spec_raper=IndexSpec.find("div",{"class":"w-dyn-list"}).find_all("div",{"role":"listitem"})
            spec_header=IndexSpec.find_all("h4",{"class":"specs-table-header-text desktop"})
            counter=0
            for modelIndex in full_spec_raper:
                spec_value=modelIndex.find_all("div",{"class":"specs-table-cell"})
                try:
                    model_length=modelIndex.find("div",{"class":"specs-dropdown-wrapper deck-links"}).text
                    if len(model_length)>1:

                        model=modelIndex.find("h2").text+" "+model_length
                        try:
                            for spname,spval in zip(spec_header,spec_value[1:]):
                                # print(specname)
                                try:
                                    specname = spname.text
                                    specvalue=spval.find("div").text
                                    if re.search(r'(?i)n/a|N/A', specvalue):
                                        pass
                                    else:
                                        if len(specvalue) > 0:
                                            if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Torque|Power', specname):
                                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                                            elif re.search(r'(?i)Operating|Pressure|Capacity|Fuel|tank|Speed|force',specname):
                                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"operational")
                                            elif re.search(r'(?i)Length|Height|Radius|Track|Width|Digging|Range',specname):
                                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"dimensions")
                                            elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure|Load',specname):
                                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"hydraulics")
                                            else:
                                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"operational")
                                        else:
                                            pass
                                except:
                                    pass

                        except:
                            pass

                        try:
                            spec2 = ProdPageSoup.find("div", {"id": "Specs"}).find("div", {"class": "full-specs-wrapper"}).find("div", {"class": "specs-collection-list-wrapper w-dyn-list"}).find_all( "div",{"role": "listitem"})[counter]
                            # for prodIndex in spec2:
                            div_cell = spec2.find_all("div", {"class": "specs-table-cell"})
                            for indexCell in div_cell:
                                specname = indexCell.find("h4", {"class": "specs-table-header-text"}).text
                                try:
                                    specvalue = indexCell.find("div").text
                                    # print("{} : {}".format(specname,specvalue))
                                    if len(specvalue) > 0:
                                        if re.search(r'(?i)n/a|N/A', specvalue):
                                            pass
                                        else:
                                            # if len(specvalue) > 0:
                                            if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Torque|Power',specname):
                                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"engine")
                                            elif re.search(r'(?i)Operating|Pressure|Capacity|Fuel|tank|Speed|force', specname):
                                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"operational")
                                            elif re.search(r'(?i)Length|Height|Radius|Track|Width|Digging|Range',specname):
                                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"dimensions")
                                            elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure|Load',specname):
                                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"hydraulics")
                                            else:
                                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"operational")
                                            # else:
                                            #     pass

                                except:
                                    pass

                        except:
                            pass

                        try:
                            # decriptn
                            dec = ProdPageSoup.find("div", {"class": "w-richtext"}).text
                            robot.Description(dec)
                        except:
                            pass

                        try:
                            Msrp = ProdPageSoup.find("div", {"class": "product-hero-right-card"}).find("div", {"class": "product-price-wrapper"}).find("div", {"class": "h6 text-space-5"})
                            robot.Msrp(Msrp.text)
                        except:
                            pass
                        ImgLst_lis_order = OrderedSet(images)
                        TempFeatList = OrderedSet(feats)
                        tempPDf=OrderedSet(Pdfs_file)
                        for pdf_index in tempPDf:
                            robot.fetch_pdf_manual(pdf_index)
                        for Indexof_union in TempFeatList:
                            if re.search(r'(?i)Option|Optional', Indexof_union):
                                robot.Options(Indexof_union)
                            else:
                                robot.Features(Indexof_union)
                        for ImgIndex_src in ImgLst_lis_order:
                            if len(ImgIndex_src) > 3:
                                if re.search(r'(?i).gif', ImgIndex_src):
                                    pass
                                else:
                                    robot.fetch_img_manual(ImgIndex_src)
                        robot.ObjectID(model)
                        robot.MasterCategory("Mowers")
                        robot.SubCategory("Zero-Turn Mowers")
                        robot.ProductUrl(productIndx)
                        robot.Country("US")
                        robot.ManufacturerName("Hustler")
                        robot.make_json()
                        counter=counter+1



                except:
                    pass
                    # model = modelIndex.find("h3").text
                    # print(model)
                    # if re.search(r'(?i)Key Specs|Engine', model):
                    #     pass
                    # else:
                        # print(model)

    except:
        pass
driver.close()
robot.destroy()









