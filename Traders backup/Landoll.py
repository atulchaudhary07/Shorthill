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
URL = "https://landoll.com/products"
robot = bot(URL)
(soup,code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
product_nav=soup.find("div",{"class":"pgafu-filtr-container"}).find_all("h2",{"class":"pgafu-post-title"})
for indexprodnav in product_nav:
    product_src= indexprodnav.find("a").get("href")
    print(product_src)
    product_name=indexprodnav.find("a").text
    driver.get(product_src)
    # driver.implicitly_wait(5)
    conten_soup=driver.page_source
    productsoup= BeautifulSoup(conten_soup,"html.parser")
    post_content=productsoup.find("div",{"class":"post-content"})
    Allimges = []
    Alloption = []
    Allfeature = []
    all_pdf=[]

    try:
        # images
        img = post_content.find_all("div", {"class": "n2-ss-slide-background n2-ow"})
        for imgIndex in img:
            imgclass = "https:" + imgIndex.find("div", {"class": "n2-ss-slide-background-image"}).get("data-desktop")
            # print(imgclass)
            Allimges.append(imgclass)

    except:
        pass
    try:
        #spec sheet
        spec_sheet=post_content.find_all("a",text="Specifications Sheet")
        for specshtIndex in spec_sheet:
            robot.fetch_pdf("https://landoll.com"+specshtIndex.get("href"))

    except:
        pass
    try: #other_images
        imgestb=post_content.find_all("img")
        for ImgIndextb in imgestb:
            srctb=ImgIndextb.get("src")
            if re.search(r'(?i).jpg', srctb):
                Allimges.append(srctb)
    except:
        pass



    try:
        # overview
        Overview_Tabs_id = post_content.find("div", {"class": "nav"}).find("a", {"id": "fusion-tab-overview"}).get("href").replace("#", "")
        ptags = post_content.find("div", {"class": "tab-content"}).find("div", {"id": Overview_Tabs_id}).find_all(["p","h3"])
        for pIndex in ptags:
            # print(pIndex.text)
            Allfeature.append(pIndex.text)

    except:
        pass
    try:
        # feature
        Features_Tabs_id = post_content.find("div", {"class": "nav"}).find("a", {"id": "fusion-tab-features"}).get("href").replace("#", "")
        # print(Features_Tabs_id)
        litgs = post_content.find("div", {"class": "tab-content"}).find("div", {"id": Features_Tabs_id}).find_all(["li", "h3"])
        for fetIndex in litgs:
            # print(fetIndex.text)
            Allfeature.append(fetIndex.text)

    except:
        pass
    try:
        # all_pdf
        main=productsoup.find("main",{"id":"main"}).find_all("a")
        for main_index in main:
            a_src=main_index.get("href")
            if re.search(r'(?i).pdf', a_src):
                all_pdf.append(a_src)
            else:
                pass


        # print(main)
    except:
        pass
    # try:
    #     # pdf
    #     spec_id = post_content.find("div", {"class": "nav"}).find("a", {"id": "fusion-tab-specs"}).get("href").replace("#", "")
    #     pdf_cont = post_content.find("div", {"class": "tab-content"}).find("div", {"id": spec_id})
    #     robot.fetch_pdf(pdf_cont)
    #
    # except:
    #     pass
    try:
        # option
        option_Tabs_id = post_content.find("div", {"class": "nav"}).find("a", {"id":"fusion-tab-options"}).get( "href").replace("#", "")
        optn = post_content.find("div", {"class": "tab-content"}).find("div", {"id": option_Tabs_id}).find_all("li")
        for opIndex in optn:
            # print(opIndex)
            Alloption.append(opIndex.text)


    except:
        pass

    try:
        # videos
        videos_Tabs_id = post_content.find("div", {"class": "nav"}).find("a", {"id": "fusion-tab-videos"}).get("href").replace("#", "")
        vid_cont = post_content.find("div", {"class": "tab-content"}).find("div", {"id": videos_Tabs_id})
        robot.fetch_videos(vid_cont)

    except:
        pass

    # try:
    #     # manuals
    #     manual_Tabs_id = post_content.find("div", {"class": "nav"}).find("a", {"id": "fusion-tab-manuals"}).get("href").replace("#", "")
    #     manual_cont = post_content.find("div", {"class": "tab-content"}).find("div", {"id": manual_Tabs_id}).find_all("a")
    #     for manualIndex in manual_cont:
    #         manual_src = manualIndex.get("href")
    #         if re.search(r'(?i)https:', manual_src):
    #             # print(manual_src)
    #             robot.fetch_pdf_manual(manual_src)
    #         else:
    #             temp_manual_src = "https://landoll.com" + manual_src
    #             robot.fetch_pdf_manual(temp_manual_src)
    # except:
    #     pass


    try:
        spec_id = post_content.find("div",{"class":"nav"}).find("a",{"id":"fusion-tab-specs"}).get("href").replace("#","")
        specs=post_content.find("div",{"class":"tab-content"}).find("div",{"id":spec_id }).find("table",{"class":"greyGridTable"})
        # print(specs)
        model_name=specs.find("thead").find_all("th")[0].text
        # print(model_name)
        if re.search(r'(?i)Model', model_name):
            model_type_1 = specs.find("tbody").find_all("tr")
            for model_typ_1_index in model_type_1:
                modeltp1=model_typ_1_index.find_all("td")[0].text

                specs_heads=[]
                thead=specs.find("thead").find_all("th")[1:]
                table_body_tr=specs.find("tbody").find_all("tr")
                #spec_heads
                for th_head in  thead:
                    specs_heads.append(th_head.text)
                    # print(th_head.text)

                #specvalues
                for tr_index in table_body_tr:
                    td=tr_index.find_all("td")[1:]
                    for sp_head_index ,td_index in zip(specs_heads,td):
                        specname=sp_head_index
                        specvalue=td_index.text
                        # print(specvalue)
                        # print("{} :  {},".format(specname,specvalue))
                        if re.search(r'(?i)n/a|N/A', specvalue):
                            pass
                        else:
                            if len(specvalue) > 0:
                                if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Torque|Power', specname):
                                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                                elif re.search(r'(?i)Length|Height|Radius|Track|Width|Digging|Range', specname):
                                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "dimensions")
                                elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure|Load', specname):
                                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "hydraulics")
                                else:
                                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "operational")
                            else:
                                pass
                try:
                    # subcat and categry
                    subcat = productsoup.find("h2").text.strip()
                    robot.SubCategory(subcat)
                    try:
                        if re.search(r'(?i)Trailer|Trailers', subcat):
                            robot.MasterCategory("Trailers")
                        elif re.search(r'(?i)Forklift|Telehandler|Construction Equipment|Farm Equipment', subcat):
                            robot.MasterCategory("Agricultural Equipment")
                        else:
                            robot.MasterCategory(subcat)

                    except:
                        pass
                except:
                    pass

                try:
                    # description

                    dec = driver.find_element_by_xpath("//h3[@class='title-heading-left fusion-responsive-typography-calculated']").text.strip()
                    # robot.Description(dec)
                    if len(dec) > 3:
                        # print(dec)
                        robot.Description(dec)
                    else:
                        Tempdesc = "Landoll" + " " + modeltp1
                        # print(dec)
                        robot.Description(Tempdesc)

                except:
                    dec = driver.find_element_by_xpath("//div[@class='fusion-text fusion-text-6']").text.strip()
                    if len(dec) > 3:
                        # print(dec)
                        robot.Description(dec)
                    else:
                        Tempdesc = "Landoll" + " " + modeltp1
                        # print(dec)
                        robot.Description(Tempdesc)


                PdfLst = OrderedSet(all_pdf)
                for pdfIndex in PdfLst:
                    if re.search(r'(?i)https:', pdfIndex):
                        robot.fetch_pdf_manual(pdfIndex)
                    else:
                        temp_manual_src = "https://landoll.com" + pdfIndex
                        robot.fetch_pdf_manual(temp_manual_src)


                ImgLst = OrderedSet(Allimges)
                for ImgIndex in ImgLst:
                    robot.fetch_img_manual(ImgIndex)

                TempFeatList = OrderedSet(Allfeature)
                for FetIndex in TempFeatList:
                    if re.search(r'(?i)n/a|N/A', FetIndex):
                        pass
                    elif re.search(r'(?i)optional|Option', FetIndex):
                        robot.Options(FetIndex)
                    else:
                        robot.Features(FetIndex)
                tempoplist = OrderedSet(Alloption)
                for indexOplst in tempoplist:
                    if re.search(r'(?i)n/a|N/A', indexOplst):
                        pass
                    else:
                        robot.Options(indexOplst)
                robot.ObjectID(modeltp1)
                robot.ProductUrl(product_src)
                robot.Country("US")
                robot.ManufacturerName("Landoll")
                robot.make_json()

        elif re.search(r'(?i)Floor Length|Length', model_name):
            model_type_2 = specs.find("tbody").find_all("tr")
            for model_typ_2_index in model_type_2:
                modeltp2 =product_name+" "+ model_typ_2_index.find_all("td")[0].text
                # print(modeltp2)

                specs_heads2 = []
                thead2 = specs.find("thead").find_all("th")[1:]
                table_body_tr2 = specs.find("tbody").find_all("tr")
                # spec_heads
                for th_head2 in thead2:
                    specs_heads2.append(th_head2.text)

                # specvalues
                for tr_index2 in table_body_tr2:
                    td2 = tr_index2.find_all("td")[1:]
                    for sp_head_index2, td_index2 in zip(specs_heads2, td2):
                        specname = sp_head_index2
                        specvalue = td_index2.text
                        # print("{}{},".format(specname,specvalue))

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
                try:
                    # subcat and categry
                    subcat = productsoup.find("h2").text.strip()
                    robot.SubCategory(subcat)
                    try:
                        if re.search(r'(?i)Trailer|Trailers', subcat):
                            robot.MasterCategory("Trailers")
                        elif re.search(r'(?i)Forklift|Telehandler|Construction Equipment|Farm Equipment', subcat):
                            robot.MasterCategory("Agricultural Equipment")
                        else:
                            robot.MasterCategory(subcat)

                    except:
                        pass
                except:
                    pass

                try:
                    # description

                    dec = driver.find_element_by_xpath("//h3[@class='title-heading-left fusion-responsive-typography-calculated']").text.strip()
                    # robot.Description(dec)
                    if len(dec) > 3:
                        # print(dec)
                        robot.Description(dec)
                    else:
                        Tempdesc = "Landoll" + " " + modeltp2
                        # print(dec)
                        robot.Description(Tempdesc)

                except:
                    dec = driver.find_element_by_xpath("//div[@class='fusion-text fusion-text-6']").text.strip()
                    if len(dec) > 3:
                        # print(dec)
                        robot.Description(dec)
                    else:
                        Tempdesc = "Landoll" + " " + modeltp2
                        # print(dec)
                        robot.Description(Tempdesc)

                PdfLst = OrderedSet(all_pdf)
                for pdfIndex in PdfLst:
                    if re.search(r'(?i)https:', pdfIndex):
                        robot.fetch_pdf_manual(pdfIndex)
                    else:
                        temp_manual_src = "https://landoll.com" + pdfIndex
                        robot.fetch_pdf_manual(temp_manual_src)


                ImgLst = OrderedSet(Allimges)
                for ImgIndex in ImgLst:
                    robot.fetch_img_manual(ImgIndex)

                TempFeatList = OrderedSet(Allfeature)
                for FetIndex in TempFeatList:
                    if re.search(r'(?i)n/a|N/A', FetIndex):
                        pass
                    elif re.search(r'(?i)optional|Option', FetIndex):
                        robot.Options(FetIndex)
                    else:
                        robot.Features(FetIndex)

                tempoplist = OrderedSet(Alloption)
                for indexOplst in tempoplist:
                    if re.search(r'(?i)n/a|N/A', indexOplst):
                        pass
                    else:
                        robot.Options(indexOplst)
                robot.ObjectID(modeltp2)
                robot.ProductUrl(product_src)
                robot.Country("US")
                robot.ManufacturerName("Landoll")
                robot.make_json()
        else:
            pass




    except:
        pass

        product_name = indexprodnav.find("a").text
        try:
            # subcat and categry
            subcat = productsoup.find("h2").text.strip()
            robot.SubCategory(subcat)
            try:
                if re.search(r'(?i)Trailer|Trailers', subcat):
                    robot.MasterCategory("Trailers")
                elif re.search(r'(?i)Forklift|Telehandler|Construction Equipment|Farm Equipment', subcat):
                    robot.MasterCategory("Agricultural Equipment")
                else:
                    robot.MasterCategory(subcat)

            except:
                pass
        except:
            pass

        try:
            # description

            dec = driver.find_element_by_xpath("//h3[@class='title-heading-left fusion-responsive-typography-calculated']").text.strip()
            # robot.Description(dec)
            if len(dec) > 3:
                # print(dec)
                robot.Description(dec)
            else:
                Tempdesc = "Landoll" + " " + product_name
                # print(dec)
                robot.Description(Tempdesc)

        except:
            dec = driver.find_element_by_xpath("//div[@class='fusion-text fusion-text-6']").text.strip()
            if len(dec) > 3:
                # print(dec)
                robot.Description(dec)
            else:
                Tempdesc = "Landoll" + " " + product_name
                # print(dec)
                robot.Description(Tempdesc)


        PdfLst = OrderedSet(all_pdf)
        for pdfIndex in PdfLst:
            if re.search(r'(?i)https:', pdfIndex):

                robot.fetch_pdf_manual(pdfIndex)
            else:
                temp_manual_src = "https://landoll.com" + pdfIndex
                robot.fetch_pdf_manual(temp_manual_src)

        ImgLst = OrderedSet(Allimges)
        for ImgIndex in ImgLst:
            robot.fetch_img_manual(ImgIndex)
        TempFeatList = OrderedSet(Allfeature)
        for FetIndex in TempFeatList:
            if re.search(r'(?i)n/a|N/A', FetIndex):
                pass
            elif re.search(r'(?i)optional|Option', FetIndex):
                robot.Options(FetIndex)
            else:
                robot.Features(FetIndex)
        tempoplist=OrderedSet(Alloption)
        for indexOplst in tempoplist:
            if re.search(r'(?i)n/a|N/A', indexOplst):
                pass
            else:
                robot.Options(indexOplst)
        robot.ObjectID(product_name)
        robot.ProductUrl(product_src)
        robot.Country("US")
        robot.ManufacturerName("Landoll")
        robot.make_json()
robot.destroy()
driver.close()




