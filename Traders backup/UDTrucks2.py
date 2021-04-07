from selenium import webdriver
from bs4 import BeautifulSoup
import requests, json, time
from ordered_set import OrderedSet
from unidecode import unidecode
from selenium.webdriver.chrome.options import Options
import sys
import re
from selenium.webdriver.support.ui import WebDriverWait
try:
    from packages import bot
except:
    sys.path.insert(0, '../')
    from packages.Crawler import bot

chrome_options = Options()
# chrome_options.add_argument("--headless")
path = r'packages/chromedriver'
driver = webdriver.Chrome(executable_path=path, options=chrome_options)
driver.maximize_window()
URL = "https://www.udtrucks.com"
robot = bot(URL)
driver.get(URL)
try:
    driver.find_element_by_xpath("//a[@class='button primary-red animated rubberBand delay-5s js-accept']").click()
except:
    pass
(soup,code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
subclass=soup.find_all("div",{"class":"promo row align-middle"})
sub_urls=[]
for subIndex in subclass:
    subclass_href=subIndex.find("a").get("href").replace("//","").strip()
    # print(subclass_href)
    sub_urls.append(subclass_href)
tempUrl=OrderedSet(sub_urls)
# tempUrl=['www.udtrucks.com/trucks/kazet']
for ProdUrl in tempUrl:
    NavUrls="https://"+ProdUrl
    # print(NavUrls)
    (nvsoup,code) = robot.get_content(NavUrls, {"method": "get", "bs4": "y"})
    # print(nvsoup)
    fets=[]
    imges=[]
    # driver.implicitly_wait(15)
    driver.get(NavUrls)
    product_name=nvsoup.find_all("span",{"class":"product-type-product-name active"})
    for mod in product_name:
        model=mod.text

        chec=driver.find_element_by_xpath("//span[text()='" + model + "']")
        driver.execute_script("arguments[0].click();", chec)
        # WebDriverWait(driver,10).until(ECdriver.find_element_by_xpath("//span[text()='" + model + "']").click()
        # try:
        #     print(driver.page_source)
        #     driver.find_element_by_xpath("//span[text()='" + model + "']").click
        # except:pass
        time.sleep(3)
        try:
            Subcat=nvsoup.find("div",{"class":"sub-nav-title show-for-large"}).text
        except:
            pass
        try:
            desc = nvsoup.find("p", {'class' : 'text-normal'}).text
        except:
            desc=""

        try:
            # features
            feat_cont=nvsoup.find_all("div",{"class":"features-container"})
            for fetIndex in feat_cont:
                try:#hi
                    h1=fetIndex.find("h1").text
                    if h1.capitalize() in fets:
                        pass
                    else:
                        fets.append(h1.capitalize())

                except:
                    pass
                try:#ptag
                    fetptag=fetIndex.find("p").text.strip()
                    if fetptag in fets:
                        pass
                    else:
                        fets.append(fetptag)
                    # print(fetptag)
                except:
                    pass

        except:
            pass

        try:
            #bar_icon_text
            barclass=nvsoup.find("div",{"class":"icon-bar product-heading-icons"}).find_all("a")
            for brAtag in barclass:
                fets.append(brAtag.text)

        except:
            pass
        try:
            # imges
            imgecont = nvsoup.find("div", {"id": "product_details_view"}).find_all("img")
            for imgIndex in imgecont:
                imgsrc = "https://www.udtrucks.com" + imgIndex.get("src")
                if re.search(r'(?i).jpg', imgsrc):
                    imges.append(imgsrc)
        except:
            pass
        try:
            elem_list = nvsoup.find_all('div', {'class': 'row row-offset'})
            for elem in elem_list:
                imgecont = elem.find_all('img')
                for imgIndex in imgecont:

                    imgsrc = "https://www.udtrucks.com" + imgIndex.get("src")
                    if re.search(r'(?i).jpg', imgsrc):
                        imges.append(imgsrc)
        except:
            pass
        try:
            elem_list=nvsoup.find_all('div',{'class':'hide-for-small-only'})
            for elem in elem_list:
                imgecont = elem.find_all('img')
                for imgIndex in imgecont:

                    imgsrc = "https://www.udtrucks.com" + imgIndex.get("src")
                    if re.search(r'(?i).jpg', imgsrc):
                        imges.append(imgsrc)
        except:pass

        # try:
        try:
            featdata=nvsoup.find_all('div',{'class':'columns small-12 cancel-padding title'})
            for feat in featdata:
                try:
                    f = feat.text.strip()
                    if f in fets:
                        pass
                    else:
                        fets.append(f)
                except:pass
        except:pass
        try:
            featdata=nvsoup.find_all('div',{'class':'columns small-12 cancel-padding subtitle'})
            for feat in featdata:
                try:
                    f = feat.find('p').text.strip()
                    if f in fets:
                        pass
                    else:
                        fets.append(f)
                except:pass
        except:pass
        try:
            featdata=nvsoup.find_all('div',{'class':'columns small-12 medium-12 cancel-padding secondary-title'})
            for feat in featdata:
                # print(feat)
                try:
                    f = feat.find('p').text.strip()
                    if f in fets:
                        pass
                    else:
                        fets.append(f)
                except:pass
        except:pass





        featdata=nvsoup.find_all('div',{'class':'promo fb-overlay'})
        for feat in featdata:
            try:
                f=feat.find('a').text.strip()
                if f.capitalize() in fets:
                    pass
                else:
                    fets.append(f.capitalize())
            except:
                pass
            try:
                f=feat.find('h1').text.strip()
                if f.capitalize() in fets:pass
                else:
                    fets.append(f.capitalize())
            except:
                pass
            try:
                f=feat.find('h2').text.strip()
                if f.capitalize() in fets:
                    pass
                else:
                    fets.append(f.capitalize())
            except:
                pass
            try:
                f=feat.find('p',{'class':'text-content'}).text.strip()
                f=unidecode(f)
                fets.append(f)
            except:
                pass
            # print(feat.find('div',{'class':'row'}))
        # except:pass
        # spec_content = driver.page_source
        # print(spec_content)

        try:
            # spec
            spec_name_list=driver.find_elements_by_xpath("//div[@class='detail-category']")
            spec_value_list = driver.find_elements_by_xpath("//div[@class='detail-value']")

            for i in range(0,len(spec_name_list)):
                specname=spec_name_list[i].text.strip()
                specvalue = spec_value_list[i].text.strip()
            # specblock=driver.find_elements_by_xpath("//div[@class='specs-block']/div[@class='details-container']")
            # for spcInd in specblock:
            #     specname=spcInd.find_element_by_xpath("/div[@class='detail-category']").text.strip()
            #     specvalue = spcInd.find_element_by_xpath("/div[@class='detail-value']").text.strip()
            # # specblock=nvsoup.find_all("div",{"class":"specs-block"})
            # for spcInd in specblock:
            #     specname= spcInd.find("div",{"class":"detail-category"}).text.strip()
            #     specvalue=spcInd.find("div",{"class":"detail-value"}).text.strip()
            #     print(specname)
            #     print(specvalue)
                if len(specvalue) > 0:
                    if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Cooling|Transmission|Power|Torque', specname):
                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                    elif re.search(r'(?i)Weight|Load', specname):
                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"weights")
                    elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure', specname):
                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"hydraulics")
                    elif re.search(r'(?i)Length|Height|Radius|Track|Width', specname):
                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"dimensions")
                    else:
                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue},"operational")
                else:
                    pass
        except:
            pass

        ImgLst = OrderedSet(imges)
        for ImgIndex in ImgLst:
            robot.fetch_img_manual(ImgIndex)
        TempFeatList = OrderedSet(fets)
        for FetIndex in TempFeatList:
            robot.Features(FetIndex)
        if desc=="":
            desc="UD Trucks"+" "+ model
        robot.ObjectID(model)
        robot.MasterCategory("Trucks")
        robot.SubCategory(Subcat)
        robot.ProductUrl(NavUrls)
        robot.Description(desc)
        robot.Country("US")
        robot.ManufacturerName("UD Trucks")
        robot.make_json()
robot.destroy()
