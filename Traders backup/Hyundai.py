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
URL = "https://www.hceamericas.com"
robot = bot(URL)
(soup, code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
li_menu = soup.find("div", {"class": "header-menu"}).find("ul", {"id": "menu-menu"}).find_all("li", recursive=False)[:6]

catlinks_lis = []
for linIndex in li_menu:
    # print(linIndex)

    try:
        cat = linIndex.find_all("a",recursive=False)
        for catindex in cat:
            cttmplink = catindex.get("href")
            # print(cttmplink)

            if re.search(r'(?i)#', cttmplink):
                pass
            else:
                if re.search(r'(?i)https:', cttmplink):
                    catlinks_lis.append(cttmplink)
                    # print(cttmplink)
                else:
                    catLink = URL + cttmplink
                    catlinks_lis.append(catLink)
                    # print(catLink)


    except:
        pass
    try:
        otherSubNav = linIndex.find_all("ul", recursive=False)
        for indexNav in otherSubNav:
            subMenu = indexNav.find_all("li",recursive=False)
            for subcat_link in subMenu:
                a_link = subcat_link.find("a").get("href")
                if re.search(r'(?i)https:|/wheeled-excavators|#|/testimonials|/leaders', a_link):
                    pass
                else:
                    subcat = URL + a_link
                    catlinks_lis.append(subcat)
    except:
        pass

Templist=OrderedSet(catlinks_lis)
for sub in Templist:
    try:
        (catcont, code) = robot.get_content(sub, {"method": "get", "bs4": "y"})
        try:
            models_tab = catcont.find("div",{"class": "model-tabs"}).find("div", {"id": "current"}).find_all("a",{"class": "hidden"})
            for mdIndex in models_tab:
                Model_name = mdIndex.text
                model_url = URL + mdIndex.get("href")
                # print(model_url)
                AllImages = []
                All_feats = []
                All_opt_lis = []


                try:
                    (modpage, code) = robot.get_content(model_url, {"method": "get", "bs4": "y"})
                    try:
                        overview = modpage.find_all("div", {"class": "col-xs-12 col-md-8"})[-1].find("p")
                        for p_tag in overview:
                            dec = p_tag.text
                            robot.Description(dec)

                    except:
                        pass
                    try:
                        model_image_overview = modpage.find("div", {"class": "main-equipment-section"}).find("img",{"class": "lowered equipment-img"}).get("src")
                        AllImages.append(model_image_overview)
                    except:
                        pass

                    try:
                        # Download_Family_Brochure
                        Download_Family_Brochure = modpage.find("a", text="Download Family Brochure").get("href")
                        robot.fetch_pdf_manual(Download_Family_Brochure)
                    except:
                        pass
                    try:
                        # Download Product Specs
                        Download_Product_Specs = modpage.find("a", text="Download Product Specs").get("href")
                        robot.fetch_pdf_manual(Download_Product_Specs)
                    except:
                        pass

                    try:
                        # std_Feature

                        main_equipmnt_feat_class = modpage.find("div", {"class": "main-equipment-section"}).find("div",{"class": "equip-hero-content equip-hero-features"}).find("div",{"class": "col-xs-12 col-md-7 features-included features-box"}).find_all("p")
                        for fet_p_tag in main_equipmnt_feat_class:
                            P_tag_fet_text=fet_p_tag.text.title().strip()
                            if len(P_tag_fet_text) is not None:
                                All_feats.append(P_tag_fet_text.replace("  "," "))


                    except:
                        pass
                    try:
                        # option

                        main_equipmnt_option_class = modpage.find("div", {"class": "main-equipment-section"}).find("div",{"class": "equip-hero-content equip-hero-features"}).find("div",{"class": "col-xs-12 col-md-7 features-custom ft-hidden features-box"}).find_all("p")
                        for opt_p_tag in main_equipmnt_option_class:
                            op_p_tag_text=opt_p_tag.text.title().strip()
                            if len(op_p_tag_text) is not None:
                                All_opt_lis.append(op_p_tag_text.replace("  "," "))
                    except:
                        pass

                    try:
                        # spec
                        spectb = modpage.find("div", {"class": "main-equipment-section"}).find("div", {"class": "equip-hero-content equip-hero-specs"}).find("div", {"class": "specs-column"}).find_all("tr")
                        for td in spectb:
                            specname = td.find_all("td")[0].text.title()
                            specvalue = td.find_all("td")[-1].text.title()
                            if re.search(r'(?i)n/a|N/A', specvalue):
                                pass
                            else:
                                if len(specvalue) > 2:
                                    if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Torque|Power', specname):
                                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"engine")
                                    elif re.search(r'(?i)Operating|Pressure|Capacity|Fuel|tank|Speed|force',specname):
                                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"operational")
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
                        # imges
                        img_scoll_section = modpage.find("div",{"id": "equip-gallery"}).find_all("div",{"class": "equip-gallery-item"})
                        for style_tag_img in img_scoll_section:
                            bck_url_img = style_tag_img.get("style")
                            tmp_bg_img = bck_url_img.replace("background-image: url(","").replace(");","")
                            AllImages.append(tmp_bg_img.strip())



                    except:
                        pass

                    try:
                        # videos
                        driver.get(model_url)
                        driver.implicitly_wait(5)
                        response = driver.page_source
                        eat_video_soup = BeautifulSoup(response, 'html.parser')
                        feat_video = eat_video_soup.find("div", {"class": "featured-video"}).find_all("iframe", {"id": "player"})
                        for Vid in feat_video:
                            vid_src = Vid.get("src")
                            robot.fetch_videos(vid_src)

                    except:
                        pass


                    try:
                        # section_features
                        page_sections_for_text = modpage.find("div", {"class": "two-col-alt"}).find_all("div", {"class": "row content-section"})
                        for tab_cont in page_sections_for_text:
                            feat_tab_data = tab_cont.find_all("div", {"class": "tca-content"})
                            for tca_class in feat_tab_data:
                                # tag_h4=tca_class.find("h4").text
                                tag_h5 = tca_class.find("h5").text.title().strip()
                                p_tag = tca_class.find("p").text.title().strip()
                                # combine_tags=tag_h4 + ":"+tag_h5+":"
                                All_feats.append(tag_h5)
                                All_feats.append(p_tag)

                    except:
                        pass

                    try:
                        # section_features_imges
                        page_sections_for_img = modpage.find("div", {"class": "two-col-alt"}).find_all("div", {"class": "row content-section"})
                        for tab_cont_img in page_sections_for_img:
                            block_class_Img = tab_cont_img.find_all("div", {"class": "image-block"})
                            for img_src_tmp in block_class_Img:
                                temp_src_img = img_src_tmp.get("style")
                                section_img_src = temp_src_img.replace("background-image: url(","").replace(");","")
                                AllImages.append(section_img_src.strip())

                    except:
                        pass

                    try:
                        sb_cat = catcont.find("h3", {"class": "dark-grey uppercase text-center"}).text
                        robot.SubCategory(sb_cat.strip())
                        try:
                            if re.search(r'(?i)Excavators|Excavator', sb_cat):
                                robot.MasterCategory("Excavators")
                            elif re.search(r'(?i)Loader|Loaders', sb_cat):
                                robot.MasterCategory("Loaders")
                            elif re.search(r'(?i)Breakers|Breaker', sb_cat):
                                robot.MasterCategory("Hammers / Breakers")
                            elif re.search(r'(?i)Tandem Drum|Single Drum ', sb_cat):
                                robot.MasterCategory("Compaction Roller")
                            else:
                                robot.MasterCategory(sb_cat)

                        except:
                            pass

                    except:
                        pass
                    try:
                        if model_url == "https://www.hceamericas.com/wheeled-excavators/hw250mh/":
                            robot.SubCategory("Wheeled Excavators")
                    except:
                        pass
                    try:
                        # class="two-col boom-industries"
                        fet_boom_industries = modpage.find("div", {"class": "two-col boom-industries"})
                        try:
                         h3_tags=fet_boom_industries.find_all("h3")
                         for h3index in h3_tags:
                             All_feats.append(h3index.text.title())
                        except:
                            pass
                        try:
                            boom_p_tags = fet_boom_industries.find_all("p")
                            for boom_p_tagindex in boom_p_tags:
                                All_feats.append(boom_p_tagindex.text.title())
                                # print(boom_p_tagindex.text.title())
                        except:
                            pass
                        try:
                            boom_imges = fet_boom_industries.find_all("img")
                            for boom_imges_index in boom_imges:
                                # All_feats.append(boom_p_tagindex.text.title)
                                AllImages.append(boom_imges_index.get("src"))
                        except:
                            pass



                    except:
                        pass
                    try:
                        # std_Feature_headings

                        main_equipmnt_feat_class_h6 = modpage.find("div", {"class": "main-equipment-section"}).find("div",{"class": "equip-hero-content equip-hero-features"}).find("div",{"class": "col-xs-12 col-md-7 features-included features-box"}).find_all("h6")
                        for fet_h6_tag in main_equipmnt_feat_class_h6:
                            h6_tag_fet_text=fet_h6_tag.text.title().strip()
                            if len(h6_tag_fet_text) is not None:
                                All_feats.append(h6_tag_fet_text.replace("  "," "))

                    except:
                        pass

                    ImgLst_lis_order = OrderedSet(AllImages)
                    TempOpList = OrderedSet(All_opt_lis)
                    TempFeatList = OrderedSet(All_feats).difference(OrderedSet(All_opt_lis))
                    for Indexof_union in TempFeatList:
                        if re.search(r'(?i)Option|Optional', Indexof_union):
                            robot.Options(Indexof_union)
                        else:
                            robot.Features(Indexof_union)
                    for ImgIndex_src in ImgLst_lis_order:
                        if len(ImgIndex_src)>3:
                            if re.search(r'(?i).gif', ImgIndex_src):
                                pass
                            else:
                                robot.fetch_img_manual(ImgIndex_src)
                    for OpIndex in TempOpList:
                        robot.Options(OpIndex)

                    robot.ObjectID(Model_name)
                    # robot.MasterCategory(category)
                    robot.ProductUrl(model_url)
                    robot.Country("US")
                    robot.ManufacturerName("Hyundai")
                    robot.make_json()

                except:
                    pass

        except:
            pass

    except:
        pass

robot.destroy()
driver.close()
