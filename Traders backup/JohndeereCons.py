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

URL = "https://www.deere.com/en/construction/"
# path = r'packages/chromedriver'
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(executable_path=path, options=chrome_options)
# driver.get(URL)
# driver.page_source
# time.sleep(10)
robot = bot(URL)
(soup,code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
nav_link=soup.find("div",{"class":"industry-sub-nav-container"}).find_all("a")[:-2]
for nav_index in nav_link:
    Url_nav_href="https://www.deere.com"+nav_index.get("href")
    # Subcat=nav_index.text
    model_URl_list=[]
    (NavSoup, code) = robot.get_content(Url_nav_href, {"method": "get", "bs4": "y"})
    try:
        first_page_data=NavSoup.find_all("div",{"data-action":"tableComp"})
        for IndexData in first_page_data:
            first_page_url=IndexData.find_all("a")
            for Url_page_index in first_page_url:
                Prod_link_first="https://www.deere.com"+Url_page_index.get("href")
                # print(Prod_link_first)
                model_URl_list.append(Prod_link_first)

    except:
        pass
    try:
        slide = NavSoup.find("div", {"class": "product-slider-wrapper"}).find_all("h4", {"class": "post-title"})
        for slide_link in slide:
            Slink = slide_link.find("a").get("href")
            (Slinksoup, code) = robot.get_content(Slink, {"method": "get", "bs4": "y"})
            slid_link_data = Slinksoup.find_all("div", {"data-action": "tableComp"})
            for IndexSlideData in slid_link_data:
                slide_Atag = IndexSlideData.find_all("a")
                for IndexAtag in slide_Atag:
                    Atag_src = "https://www.deere.com"+IndexAtag.get("href")
                    model_URl_list.append(Atag_src)
    except:
        pass

    try:
        #scrappr_cat_trck
        page_cta=NavSoup.find_all("div",{"class":"image-wrapper"})[:-2]
        for IndexPage_cta in page_cta:
            page_atag="https://www.deere.com"+IndexPage_cta.find("a").get("href")
            (page_atagSoup, code) = robot.get_content(page_atag, {"method": "get", "bs4": "y"})
            try:
                scpr_link=page_atagSoup.find_all("div",{"data-action":"tableComp"})
                for IndexScp in scpr_link:
                    scrapr_tagA=IndexScp.find_all("a")
                    for index_tagA_scrp in scrapr_tagA:
                        scr_tagA_srcp="https://www.deere.com"+index_tagA_scrp.get("href")
                        # print(scr_tagA_srcp)
                        model_URl_list.append(scr_tagA_srcp)
            except:
                pass
            try:
                another_scpr_nav=page_atagSoup.find("div",{"data-action":"modelListingComp"}).find_all("h3",{"class":"model"})
                for index_srp_nav in another_scpr_nav:
                    href_nav="https://www.deere.com"+index_srp_nav.find("a").get("href")
                    # print(href_nav)
                    model_URl_list.append(href_nav)


            except:
                pass

    except:
        pass



    try:
        #nesting_page
        nav_nesting=NavSoup.find_all("div",{"class":"component content-panel with-image"})
        # print(nav_nesting)
        for nesting_index in nav_nesting:
            nested_Url="https://www.deere.com"+nesting_index.find("a").get("href")
            (NestedSoup, code) = robot.get_content(nested_Url, {"method": "get", "bs4": "y"})
            nest_prod_links_data=NestedSoup.find_all("div",{"data-action":"tableComp"})
            for IndexNst in nest_prod_links_data:
                nest_prod_links=IndexNst.find_all("a")
                for nest_index in nest_prod_links:
                    prodUrl_on_nest=nest_index.get("href")
                    if re.search(r'(?i)https://www.deere.com', prodUrl_on_nest):
                        model_URl_list.append(prodUrl_on_nest)
                    else:
                        model_URl_list.append("https://www.deere.com"+prodUrl_on_nest)
    except:
        pass
    Models_Url=OrderedSet(model_URl_list)
    # print(len(Models_Url))

    for mod_url in Models_Url:
        (product_page, code) = robot.get_content(mod_url, {"method": "get", "bs4": "y"})
        content_class=product_page.find("div",{"data-action":"productSummaryComp"})
        feats_lis=[]
        images_lis=[]
        Option_lis=[]
        other_fet=[]
        Pdf_lis=[]
        model_name=content_class.find("span",{"class":"model"}).text
        subcat=content_class.find("span",{"class":"category"}).text
        try:
            price=content_class.find("span",{"class":"value"}).text
            robot.Msrp(price)
        except:
            pass
        try:
            # robot.fetch_pdf(content_class)
            Pdf_src_cont=content_class.find("div",{"class":"links-section"}).find_all("a")
            for Pdf_a in Pdf_src_cont:
                pdf=Pdf_a.get("href")
                if re.search(r'(?i)financial|dealerlocator|#tag-compare|forms', pdf):
                    pass
                else:
                    if re.search(r'(?i)https://www.deere.com',pdf):
                        Pdf_lis.append(pdf)
                        # robot.fetch_pdf_manual(pdf)
                        # print(pdf)
                    else:
                        Pdf_lis.append("https://www.deere.com"+pdf)
                        # robot.fetch_pdf_manual("https://www.deere.com"+pdf)
                        # print("https://www.deere.com"+pdf)
        except:
            pass
        # try:
        #     Pdf2=product_page.find("a",text='View Product Brochure').get("href")
        #     if re.search(r'(?i)https://www.deere.com', Pdf2):
        #         robot.fetch_pdf_manual(Pdf2)
        #     else:
        #         robot.fetch_pdf_manual("https://www.deere.com"+Pdf2)
        # except:
        #     pass
        # try:
        #     Pdf3=product_page.find("a",text='View Attachments Brochure').get("href")
        #     if re.search(r'(?i)https://www.deere.com', Pdf3):
        #         robot.fetch_pdf_manual(Pdf3)
        #     else:
        #         robot.fetch_pdf_manual("https://www.deere.com"+Pdf3)
        # except:
        #     pass

        try:
            #images
            img=content_class.find_all("img")
            for img_index in img:
                src="https://www.deere.com"+img_index.get("src")
                images_lis.append(src)

        except:
            pass
        try:
            #images
            imges_section=product_page.find_all("div",{"class":"seccion-images"})
            for section_index in imges_section:
                img_section_src=section_index.find("img").get("src")
                images_lis.append(img_section_src)
        except:
            pass
        try:
            Fet_img_col=product_page.find("div",{"data-action":"expandCollapseComponent"}).find_all("img")
            for FetimgIndex in Fet_img_col:
                images_lis.append(FetimgIndex.get("src"))
        except:
            pass



        try:
            # images_section_text
            imges_section_text = product_page.find_all("div", {"class": "seccion-images"})
            for section_index_text in imges_section_text:
                # print(section_index_text)
                img_section_text = section_index_text.find_all(["p","li"])
                for indexTxt in img_section_text:
                    other_fet.append(indexTxt.text)
        except:
            pass


        try:
            #details
            class_detail=content_class.find("div",{"class":"details"}).find_all("li")
            for li in class_detail:
                text_li=li.text.strip()
                try:
                    if re.search(r'(?i):', text_li):
                        li_split=text_li.split(':')
                        specname=li_split[0].strip()
                        specvalue=li_split[-1].strip()
                        if len(specvalue) > 0:
                            if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Cooling', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                            elif re.search(r'(?i)Operating|Pressure|Capacity|Fuel|tank|Speed', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "operational")
                            elif re.search(r'(?i)Length|Height||Radius|Track|Width|Load', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "dimensions")
                            elif re.search(r'(?i)Weight|Load', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "weights")
                            elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "hydraulics")
                            else:
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "other")
                        else:
                            pass

                    else:
                        feats_lis.append(li.text)

                except:
                    pass

                    # feats_lis.append(li.text)

        except:
            pass


        try:
            #feature
            fet_class=product_page.find("div",{"data-action":"expandCollapseComponent"}).find_all("p")
            for ptag in fet_class:
                ptag_text=ptag.text.splitlines()
                for Index_P_tag in ptag_text:
                    # print(Index_P_tag)
                    if re.search(r'(?i)Optional',Index_P_tag):
                        Option_lis.append(Index_P_tag)
                    else:
                        feats_lis.append(Index_P_tag)

        except:
            pass
        try:
            #feature_g-scrollable
            fet_class_g_scrollable=product_page.find("div",{"data-action":"expandCollapseComponent"}).find_all("table")
            for scrollable_index in fet_class_g_scrollable:
                # print(scrollable_index)
                ptag_text=scrollable_index.find_all("p")
                for Index_P_tag in ptag_text:
                    other_fet.append(Index_P_tag.text)
                #     P_tag_li=Index_P_tag.text.strip().split("\n")
                #     for index_in_p_tag in P_tag_li:
                #         print(index_in_p_tag)

        except:
            pass


        try:
            #feature
            fet_class_li=product_page.find("div",{"data-action":"expandCollapseComponent"}).find_all("li")
            for li_tag in fet_class_li:
                li_text=li_tag.text.strip()
                if re.search(r'(?i)Optional',li_text):
                    Option_lis.append(li_text)
                else:
                    feats_lis.append(li_text)
            # feats_lis.append(li_tag.text)
        except:
            pass

        try:
            #Videos
            Vid_scp=product_page.find_all("div",{"class":"video-player-comp video-wrapper"})
            for vid in Vid_scp:
                iframe=vid.find("iframe").get("src")
                robot.fetch_videos(iframe)

        except:
            pass

        try:
            #spec
            spec_class=product_page.find("div",{"data-action":"specificationsComp"}).find_all("div",{"class":"table-container"})

            for sptable in spec_class:

                table_tr=sptable.find("tbody")
                if table_tr is None:
                    pass
                else:
                    tr=table_tr.find_all("tr")
                    for tr_index in tr:
                        specname=tr_index.find("th").text
                        specvalue=tr_index.find("td").text
                        if re.search(r'(?i)n/a|N/A|no|No', specvalue):
                            pass
                        elif re.search(r'(?i)yes|Yes', specvalue):
                            feats_lis.append(specname)
                        elif re.search(r'(?i)Optional|Option', specvalue):
                            Option_lis.append(specname+" "+specvalue)
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
        dec = "John Deere" + " " + model_name
        robot.Description(dec)
        TempFeatList = OrderedSet(feats_lis).difference(OrderedSet(other_fet))
        for FetIndex in TempFeatList:
            robot.Features(FetIndex)
        ImgLst = OrderedSet(images_lis)
        for ImgIndex in ImgLst:
            if re.search(r'(?i)gif', ImgIndex):
                pass
            else:
                robot.fetch_img_manual(ImgIndex)
        TempOpList = OrderedSet(Option_lis)
        for OpIndex in TempOpList:
            robot.Options(OpIndex)
        temppdfc=OrderedSet(Pdf_lis)
        for pdf_index in temppdfc:
            robot.fetch_pdf_manual(pdf_index)
        robot.ObjectID(model_name)
        robot.SubCategory(subcat)
        robot.MasterCategory("Construction")
        robot.ProductUrl(mod_url)
        robot.Country("US")
        robot.ManufacturerName("John Deere")
        robot.make_json()
robot.destroy()
