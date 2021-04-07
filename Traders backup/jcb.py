import re, datetime, sys
from unidecode import unidecode

try:
    from packages.Crawler import bot
except:
    sys.path.insert(0, '../')
    from packages.Crawler import bot

URL = "https://www.jcb.com/en-us/"
URL_1 = "https://www.jcb.com/"
robot = bot(URL)
(content, code) = robot.get_content(URL, {"method": "get", "bs4": "y"})
(contSoup, code) = robot.get_content(URL_1, {"method": "perl", "bs4": "y"})

product_data = content.find('ul', {'class': "navbar-nav"})
for n in product_data.find_all('li'):
    tag = n.find('a').get('href')
    if tag is None: continue
    tag = URL_1 + tag
    MasterCategory = n.find('a')
    if MasterCategory is None: continue
    MasterCategory = MasterCategory.getText(' ')
    (mastercont, code) = robot.get_content(tag, {"method": "get", "bs4": "y"})
    for subcont in mastercont.find_all('div', {'class': 'col-12 col-sm-6 col-md-6 col-lg-4 col-xl-3'}):
        tag2 = URL_1 + subcont.find('a').get('href')
        if tag2 is None: continue
        Subcategory = subcont.find('a').find('figcaption').getText(' ')
        print(tag2)
        (subcnt, code) = robot.get_content(tag2, {"method": "get", "bs4": "y"})
        if subcnt is None: continue
        for s in subcnt.find_all('div', {'class': 'product-list'}):
            product_link = s.find('a').get('href')
            if product_link is None: continue
            product_link = URL_1 + product_link
            (innerCont, code) = robot.get_content(product_link, {"method": "get", "bs4": "y"})
            model = innerCont.find('h1', {'class': 'compo-title'})
            Description = innerCont.find('div', {'class': 'visible-copy'})
            if Description is None: continue
            Description = Description.getText(" ")
            robot.ObjectID(model)
            robot.ProductUrl(product_link)
            robot.Description(Description)
            robot.ManufacturerName("JCB")
            robot.MasterCategory(MasterCategory)
            robot.Subcategory(Subcategory)
            robot.Country("US")
            fetcot = innerCont.find('div', {'class': 'list-items'})
            if fetcot is not None:
                fetcot = fetcot.find('ul')

                for fet_desc in fetcot.findAll("li"):
                    Features = fet_desc.getText().strip()
                    robot.Features(Features)

            for fet in innerCont.find_all('div', {'class': 'single-block-only'}):
                if (re.search(r'<style', str(fet))): continue
                fetCont = fet.getText("!@!@!")
                for j in fetCont.split("!@!@!"):
                    robot.Features(j)

            for spec in innerCont.find_all('div', {'class': 'col-4'}):
                specnameh = spec.find('div', {'class': 'spec-header'}).getText()
                specnamed = spec.find('div', {'class': 'spec-details'}).getText()
                specname = specnameh
                specvalue = specnamed
                if (re.search(r'(?i)engine', specname)):
                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                elif (re.search(r'(?i)cutting|deck', specname)):
                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "operation")
                elif (re.search(r'(?i)width|height|depth|weight', specname)):
                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "dimension")
                else:
                    robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "others")

            for j in innerCont.find_all("iframe", {"src": re.compile(r'.+youtube.+')}):
                robot.fetch_videos(j.get("src"))
            img_cont = innerCont.find("div", {"class": "media-box"})
            if (img_cont is not None):
                for j in img_cont.find_all("a", {"href": re.compile(r'youtu')}):
                    robot.fetch_videos(j.get("href"), "")

            im = innerCont.find('div', {'class': 'jcb-hero-img'}).get('style')
            im = re.match(r'.+?url\((.+?)\)', im)
            src = im.group(1)
            robot.fetch_img_manual(URL_1 + src)
            for g in innerCont.find_all("img", {"class": "gallery-image"}):
                robot.fetch_img_manual(URL_1 + g.get("src"))

            robot.make_json()

robot.destroy()