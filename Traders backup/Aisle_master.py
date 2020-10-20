# importing modules
import sys
import re
from ordered_set import OrderedSet
try:
    from packages.Crawler import bot
except:
    sys.path.insert(0, '../')
    from packages.Crawler import bot

URL = "https://www.aisle-master.com/products/"
robot = bot(URL)         # making object of bot class
(soup,code) = robot.get_content(URL, {"method": "get", "bs4": "y"})  # sending the request to page with parameters
# print(soup)

subclass= soup.find_all("li",{"class":"firstItem"})    #finding all product's link
sub_urls=[]

for subIndex in subclass:       # cleaning url's one by one
    subclass_href=subIndex.find("a").get("href")     # getting href links
    sub_urls.append(subclass_href)       # href links for each product
    # print(subclass_href)

# print(sub_urls)
tempUrl= OrderedSet(sub_urls)    # remove dupliate links in order

for NavUrls in tempUrl:      ## traversing each product info one by one
    (nvsoup,code) = robot.get_content(NavUrls, {"method": "get", "bs4": "y"})  # sending the request to url with parameters
    # print(nvsoup)
    fets=[]       # list to store features
    imges=[]      # list to store images
    description = []  # empty string to store description

    product_name= nvsoup.find('h1').text.strip()
    subcat = product_name   # product's sub-category
    print(subcat)

    ## getting description
    try:
        descrip_block = nvsoup.find('div', class_= 'woocommerce-product-details__short-description')
        para = descrip_block.findAll('p')
        for p in para:
             description.append(p.text.strip())
        # print(description)
    except:
        pass

    ## getting features
    try:
        descrip_block = nvsoup.find('div', class_= 'woocommerce-product-details__short-description')
        feat = descrip_block.findAll('li')
        for li in feat:
            fets.append(li.text.strip())
        # print(fets)
    except:
        pass

    ## getting images
    try:
        imgecont = nvsoup.find('div', {"class": "col-lg-6 col-md-6 col-sm-12 product-images"}).findAll('img')
        for imgIndex in imgecont:
            imgsrc= imgIndex.get("src")
            if re.search(r'(?i).jpg', imgsrc):  ## append only .jpg links
                imges.append(imgsrc)
        print(imges)
    except:
        pass

    ## getting specifications
    try:
        table = nvsoup.find('table', class_='woocommerce-product-attributes shop_attributes')
        if table != None:
            spec = table.findAll('tr')
            for tr in spec:    ## traversing each 'tr' to get specification name and its value
                specname= tr.find('th').text.strip()
                specvalue= tr.find('td').text.strip()
                if len(specvalue) > 0:
                    if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Cooling', specname):
                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                    elif re.search(r'(?i)Length|Height|Radius|Track|Width|Load', specname):
                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "dimensions")
                    elif re.search(r'(?i)Weight|Load', specname):
                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "weights")
                    elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure', specname):
                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "hydraulics")
                    else:
                        robot.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "operational") ## changes
                else:
                    pass
        else:
            ## if any video occur, store its url
            vid = nvsoup.find('iframe').get('src')
            robot.fetch_videos(vid)
            print(vid)
    except:
        pass

## put data in json object
    ImgLst = OrderedSet(imges)  ## images object
    for ImgIndex in ImgLst:
        robot.fetch_img_manual(ImgIndex)

    TempFeatList = OrderedSet(fets)   ## features object
    for FetIndex in TempFeatList:
        robot.Features(FetIndex)
    tempdes="".join(description)
    model= product_name
    robot.ObjectID(model)
    robot.MasterCategory("Lifting Equipment")
    robot.SubCategory(subcat)
    robot.ProductUrl(NavUrls)
    robot.Description(tempdes)
    robot.Country("US")
    robot.ManufacturerName("Aisle Master Lifting Innovation")

## creating json file
    robot.make_json()
robot.destroy()   ## freed occupied memory

