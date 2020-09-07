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
URL="https://www.rightline.com"
# URL = "https://www.rightline.com/attachments/"
robot = bot(URL)
(soup, code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
Drop_down=soup.find("div",{"id":"navbarNavDropdown"}).find("ul",{"class":"dropdown-menu"}).find_all("li",recursive=False)
model_url = []
for dropdown in Drop_down:
    drop_a = dropdown.find_all("a")
    for link in drop_a:
        subcat_link = URL + link.get("href").strip()
        model_url.append(subcat_link)



order_model=OrderedSet(model_url)
for Model_Url_indexing in order_model:
    driver.get(Model_Url_indexing)
    driver.implicitly_wait(7)
    page_response = driver.page_source
    sbcat_page_soup = BeautifulSoup(page_response, 'html.parser')
    spec_tabs = sbcat_page_soup.find("div", {"id": "specification-table"}).find_all("div", {"class":"product-table"})
    for spectable in spec_tabs:
        model_names_tabel = spectable.find_all("table")
        for table in model_names_tabel:
            specname_list = []
            th = table.find("thead").find_all("tr")[0].find_all("th")[1:]
            th_2=table.find("thead").find_all("tr")[-1].find_all("th")[1:]
            for th_index,th_head in zip(th,th_2):

                # specname_list.append(th_index.text)
                if th_head.text is None:
                    specname_list.append(th_index)
                else:
                    specname_list.append(th_index.text + th_head.text)
            tablebody = table.find("tbody").find_all("tr")
            for tds in tablebody:
                Sub_heading = spectable.find("h4").text.replace(" | ","|")
                model = tds.find("td").text.strip()+" "+ Sub_heading
                td_text = tds.find_all("td")[1:]
                subcat=sbcat_page_soup.find("section",{"class":"texty-10 mb-20"}).find("h1").text.title().strip()
                feat_list = []
                Images_list = []
                Options_list = []

                OrderSpecList = OrderedSet(specname_list)
                for SpecNm, SpecVal in zip(OrderSpecList, td_text):
                    specname = SpecNm.title().replace("Iii","III").replace("Ii","II")
                    specvalue = SpecVal.text
                    if re.search(r'(?i)n/a|N/A|login',specvalue):
                        pass
                    else:
                        if len(specvalue)>0:
                            if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Torque|Power', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                            elif re.search(r'(?i)Operating|Pressure|Capacity|Fuel|tank|Speed|force', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"operational")
                            elif re.search(r'(?i)Length|Height|Radius|Track|Digging|Range|Size|Thickness|Width', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"dimensions")
                            elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure|Load', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"hydraulics")
                            else:
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"operational")
                        else:
                            pass
                try:
                    # description
                    dec = sbcat_page_soup.find("h3", {"class": "text-secondary-gray"}).text.strip()
                    robot.Description(dec.replace("Iii","III").replace("Ii","II"))

                except:
                    pass
                try:
                    # features
                    fet_section = sbcat_page_soup.find("section", {"id": "feature"}).find_all("div", {"class": "texty-3 mb-20"})
                    try:
                        for ft in fet_section:
                            try:
                                # heading
                                Heading = ft.find("h1").text.strip()
                                feat_list.append(Heading)
                            except:
                                pass
                            try:
                                # ptag
                                ptag = ft.find_all("p")
                                for ptext in ptag:
                                    feat_list.append(ptext.text)
                            except:
                                pass
                            try:
                                # li
                                li = ft.find_all("li")
                                for liIndex in li:
                                    feat_list.append(liIndex.text)

                            except:
                                pass


                    except:
                        pass

                except:
                    pass

                try:
                    # Images
                    picture_class = sbcat_page_soup.find_all("picture")
                    for picture_index in picture_class:
                        img_src = picture_index.find("img").get("srcset")
                        Images_list.append(img_src)

                except:
                    pass

                try:
                    # option
                    op = sbcat_page_soup.find("section", {"class": "text-container text-container-1080px"})
                    try:
                        # option_h3_heading_in_white
                        op_h3_class = op.find_all("h3")
                        for Op_h3_index in op_h3_class:
                            Options_list.append(Op_h3_index.text)

                    except:
                        pass

                    try:
                        # option_container_text
                        option_p_tag = op.find_all("p")
                        for Op_p_index in option_p_tag:
                            Options_list.append(Op_p_index.text)

                    except:
                        pass

                except:
                    pass

                # try: #WarrntyPDF
                #     pdf_page_url=URL+sbcat_page_soup.find("a",text="Warranty Statement").get("href")
                #     (pdf_soup,code) =robot.get_content(pdf_page_url,{"method": "get", "bs4": "y"})
                #     pdf_src=pdf_soup.find("div",{"class":"main"})
                #     robot.fetch_pdf(pdf_src)
                #
                # except:
                #     pass
                if re.search(r'(?i)Bale Clamp|Rotating Bale Clamp|Folding Arm Bale Clamp|Bar Arm Clamp|Broke Clamp Hold Down|Carton Clamp|Tipping Carton Clamp|Drum Clamp|Rotating Drum Clamp|Forward Tipping Drum Clamp|Foam Clamp|Fork Clamp|Rotating Fork Clamp|Folding Fork Clamp|Gaylord Clamp|General Purpose Clamps|Rotating General Purpose Clamp|Insulation Clamp|Paper Roll Clamp|Razorback Clamp|Tire Distribution Clamp', subcat):
                    robot.MasterCategory("Clamp")
                elif re.search(r'(?i)H-Series Fork Positioner|G-Series Fork Positioner|Hook to Shaft Fork Positioner|Lateral Fork Positioner|Integral Fork Positioner', subcat):
                    robot.MasterCategory("Fork Positioners")
                elif re.search(r'(?i)Side Shifter|Hook to Shaft Sideshifter|Double Side Shifter|Integral Sideshifter',subcat):
                    robot.MasterCategory("Side Shifter")
                elif re.search(r'(?i)Block Handler|Integral Double Block Handler',subcat):
                    robot.MasterCategory("Block Handler ")
                elif re.search(r'(?i)Hang-On Adapter Carriage', subcat):
                    robot.MasterCategory("Adapter Carriage")
                elif re.search(r'(?i)ITA Carriage Bar', subcat):
                    robot.MasterCategory("Carriage Bar")
                elif re.search(r'(?i)Fork Bar Rotator', subcat):
                    robot.MasterCategory("Rotator")
                elif re.search(r'(?i)Bin Dumper', subcat):
                    robot.MasterCategory("Dumper")
                elif re.search(r'(?i)Load Backrests', subcat):
                    robot.MasterCategory("Load Backrests")
                elif re.search(r'(?i)Vertical Load Stabilizer|Broke Clamp Hold Down', subcat):
                    robot.MasterCategory("Load Stabilizers")
                elif re.search(r'(?i)Single Double Pallet Handler|Single Dual Stabilizer', subcat):
                    robot.MasterCategory("Single Double")
                elif re.search(r'(?i)Slope Piler', subcat):
                    robot.MasterCategory("Slope Piler")
                elif re.search(r'(?i)Flexible Bag Handler', subcat):
                    robot.MasterCategory("Flexible Bag Handler")
                elif re.search(r'(?i)Push Pull|Load Push', subcat):
                    robot.MasterCategory("Push Pull")
                elif re.search(r'(?i)ITA Forks|Shaft Mount Forks', subcat):
                    robot.MasterCategory("Forks")
                else:
                    robot.MasterCategory("Attachments")


                ImgLst = OrderedSet(Images_list)
                for ImgIndex in ImgLst:
                    new_src_img_link=ImgIndex.split("?date")[0]
                    robot.fetch_img_manual(new_src_img_link)
                TempFeatList = OrderedSet(feat_list)
                for FetIndex in TempFeatList:
                    fet_replce=FetIndex.title().replace("Iii","III").replace("Ii","II")
                    robot.Features(fet_replce)
                TempOpList = OrderedSet(Options_list)
                for OpIndex in TempOpList:
                    op_replce=OpIndex.title().replace("Iii","III").replace("Ii","II")
                    robot.Options(op_replce)

                robot.ObjectID(model)
                robot.SubCategory(subcat.replace("Iii","III").replace("Ii","II"))
                robot.ProductUrl(Model_Url_indexing)
                robot.Country("US")
                robot.fetch_pdf_manual("https://www.rightline.com/static/warranty.pdf")
                robot.ManufacturerName("Rightline")
                robot.make_json()
robot.destroy()
driver.close()
