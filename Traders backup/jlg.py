from selenium import webdriver
from bs4 import BeautifulSoup
import requests, json,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ordered_set import OrderedSet
chrome_options = Options()
chrome_options.add_argument("--headless")
path = r'packages/chromedriver'
driver = webdriver.Chrome(executable_path=path,options=chrome_options)
# driver=webdriver.Chrome(path)
driver.get('https://www.jlg.com/en/equipment')
response=driver.page_source
soup=BeautifulSoup(response,'html.parser')
url="https://www.jlg.com"
cat=soup.find("div",{"class":"row contentRow equipRow"}).find_all("div",{"class":"col-xs-6 col-sm-4 equipBlock"})
# element=driver.find_element_by_xpath("//*[@class='row contentRow equipRow']")
# all=element.find_elements_by_xpath("//*[@id='Eng']")
models_link=[]
templist=[]
for ctlink in cat:
    link=url + ctlink.find("a").get("href")
    cat_name=ctlink.find("div",{"class":"equipName"}).text
    driver.get(link)
    cat_link_response=driver.page_source
    cat_link_soup=BeautifulSoup(cat_link_response,'html.parser')
    subcatlink=cat_link_soup.find("div",{"class":"container contentRow"}).find_all("div",{"class":"famCatViewModels"})
    subcat_name=cat_link_soup.find("div",{"class":"container contentRow"}).find_all("h3")
    for sbct,sb_name in zip(subcatlink,subcat_name):
        sublink=url+sbct.find("a").get("href")
        subcatName=sb_name.text.strip()
        driver.get(sublink)
        driver.implicitly_wait(15)

        sb_page_source=driver.find_elements_by_xpath("//div[@data-bind='text:name']")

        for modelNm in sb_page_source:
            Tmpmodel=modelNm.text.split(" ")
            model="-".join(Tmpmodel)
            model_link=sublink+"/"+model
            templist.append(model_link)



for tmp in templist:
    try:
        driver.get(tmp)
        driver.implicitly_wait(15)
        model_series_page=driver.find_elements_by_xpath("//div[@data-bind='text: Name']")
        for mod in model_series_page:
            srMod=mod.text.split(" ")
            submodel="-".join(srMod)
            mod_url=tmp+"/"+submodel
            models_link.append(mod_url)
    except:
        models_link.append(tmp)
#model_links
for modlink in models_link:
    print(modlink)


