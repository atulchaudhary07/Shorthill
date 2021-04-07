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
URL = "https://www.talbertmfg.com/showrooms/Talbert/"
robot = bot(URL)
driver.get(URL)
time.sleep(5)
Showroom=driver.find_element_by_xpath('//div[@id="showroom-model-year-2021"]').find_elements_by_tag_name("a")
producd_Urls=[]
for index in Showroom:
    product_link=index.get_attribute("href")
    producd_Urls.append(product_link)
temp_url=OrderedSet(producd_Urls)
for Index_url in temp_url:
    print("fetching : "+ Index_url)
    driver.get(Index_url)
    time.sleep(5)
    response=driver.page_source
    productsoup = BeautifulSoup(response, "html.parser")
    imges=[]
    model = []
    Cate=[]
    subcat=[]
    prodyear=[]
    manufct=[]


    try:
        infotab=productsoup.find("div",{"id":"info"}).find("table").find("tbody").find_all("tr")
        for TrIndex in infotab:
            key=TrIndex.find_all("td")[0].text
            value=TrIndex.find_all("td")[-1].text

            try:
                if re.search(r'(?i)Manufacturer', key):
                    manufacturername=value
                    manufct.append(manufacturername)
                    # robot.ManufacturerName(manufacturername)
            except:
                pass

            try:
                if re.search(r'(?i)Model',key):
                    modelname=value
                    model.append(modelname)
                    # robot.ObjectID(modelname)
            except:
                pass
            try:
                if re.search(r'(?i)Year', key):
                    manufactureryear=value
                    prodyear.append(manufactureryear)
                    # robot.Year(manufactureryear)
            except:
                pass
            try:
                if key=="Category":
                    category=value
                    Cate.append(category)
            except:
                pass

            try:
                if key=="Subcategory":
                    subcategory=value
                    subcat.append(subcategory)
                    # robot.SubCategory(subcategory)
            except:pass

    except:
        pass
    try:
        disclaimer = productsoup.find("p", {"class": "msrp-disclaimer"}).text
        robot.Options(disclaimer)
    except:
        pass

    try:
        sepc_tab = productsoup.find("div", {"id": "specs"}).find_all("table")
        for table_index in sepc_tab:
            tr = table_index.find("tbody").find_all("tr")
            for td in tr:
                specname = td.find_all("td")[0].text
                specvalue = td.find_all("td")[-1].text
                # print(specvalue)
                # print(specname)
                if re.search(r'(?i)n/a|N/A', specvalue):
                    pass

                else:
                    if re.search(r'(?i)feature',specname):
                        robot.Features(specname+":"+specvalue)
                    else:
                        if len(specvalue) > 0:
                            if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Torque|Power', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                            elif re.search(r'(?i)Length|Height|Radius|Track|Width|Digging|Range', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "dimensions")
                            elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure|Load', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "hydraulics")
                            elif re.search(r'(?i)Electrical', specname):
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "electrical")
                            else:
                                robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "operational")
                        else:
                            pass
    except:
        pass

    try:
        # image
        img = productsoup.find("div", {"id": "model-image"}).find_all("img")
        for imgesIndex in img:
            img_src = imgesIndex.get("src")
            imges.append(img_src)
    except:
        pass

    try:
        # pdf
        PDF = productsoup.find("a", text="View OEM Brochure").get("href")
        robot.fetch_pdf_manual(PDF)

    except:
        pass

    ImgLst_lis_order = OrderedSet(imges)
    for ImgIndex_src in ImgLst_lis_order:
        robot.fetch_img_manual(ImgIndex_src)

    tempMod = "".join(model)
    tempYear = "".join(prodyear)
    tempcate = "".join(Cate)
    temSubcat = "".join(subcat)
    tempmanufct = "".join(manufct)

    desc= tempmanufct +" "+tempMod
    robot.Description(desc)


    robot.ObjectID(tempMod)
    robot.Year(int(tempYear))
    robot.SubCategory(temSubcat)
    robot.MasterCategory(tempcate)
    robot.ProductUrl(Index_url)
    robot.Country("US")
    robot.ManufacturerName(tempmanufct)
    robot.make_json()
robot.destroy()
driver.close()




