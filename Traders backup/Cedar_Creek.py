# importing modules
import re
import sys
from ordered_set import OrderedSet

try:
    from packages.Crawler import bot
except BaseException:
    sys.path.insert(0, '../')
    from packages.Crawler import bot


def get_product_url(res):
    """get product's clean urls"""

    links = []
    for a in res.findAll('a', href=True):
        if 'rvs/' in a['href']:
            links.append('https:' + a['href'])

    return OrderedSet(links)


#######################################

def general_page_scraping(sp):
    """getting general information about product, #category, subcat, description, features, options, product_links"""

    # category
    global category, subcat, description, features, options, model_links

    try:
        cat_block = sp.find("span", {"class": "text-uppercase text-dosis page-nav-title page-nav-open"}).text.strip()
        category = cat_block.rsplit('\t')[-1]
        print(category)
    except BaseException as e:
        print(e)
        pass

    # sub-category
    try:
        sub_block = sp.find('h3', {"class": "text-large clear-fix pt-4"})
        subcat = sub_block.text.strip()
        print(subcat)
    except BaseException:
        pass

    # description
    try:
        desc_block = sp.find('div', {"id": "about"}).find('p')
        description = desc_block.text.strip()
        # print(description)
    except BaseException:
        pass

    # features and options
    try:
        feat_block = sp.find('div', {"id": "accordionGenFeatures"})
        cards = feat_block.findAll('div', {"class": "card float-left feature-item"})

        # header = feat_block.findAll('div', {"class": "card-header"})
        # features_head = [div.text.strip() for div in header]  # feature's header

        feature_card = cards[:-1]
        option_card = cards[-1]

        features = []
        for div in feature_card:
            temp = [li.text.strip() for li in div.findAll('li')]
            features.extend(temp)
            temp.clear()

        print(len(features))
        options = [li.text.strip() for li in option_card.findAll('li')]
        # print(options)
        print(len(options))
    except BaseException:
        pass

    # getting models links under specific category
    try:
        web_link = []
        a = category.lower().replace(' ', '-') + '/'
        all_models = sp.find('div', id="floorplans")

        for link in all_models.findAll('a', href=True):
            if a in link['href'] and ('rvs' not in link['href']):
                web_link.append('https://forestriverinc.com/rvs/fifth-wheels/' + link['href'])
        # print(web_link)

        model_links = OrderedSet(web_link)
        # print(model_links)
    except BaseException:
        pass

    return category, subcat, description, features, options, model_links


#####################################

def model_page_scraping(s, rob):
    """getting specific info about model # return model,producturl,temp_imag,specific_name,spacific_value,operat,video
"""
    # link = 'https://forestriverinc.com/rvs/fifth-wheels/cedar-creek-champagne-edition/38EL/2768'
    # link= 'https://forestriverinc.com/rvs/fifth-wheels/cedar-creek/311RL/5606'

    try:
        model = s.findAll('h2')[0].text.strip().split()[0]
        rob.ObjectID(model)
        print(model)
    except BaseException:
        pass

    # specifications
    try:
        specname = ""
        sp = s.findAll('div', class_='specification-cell')
        if sp is not None:
            for ind, cell in enumerate(sp):
                if ind % 2 == 0:  # one by one
                    specname = cell.text.strip().replace(':', '')
                else:
                    specvalue = cell.text.strip()
                    # print(specname)
                    # print(specvalue)

                    if len(specvalue) > 0:
                        if re.search(r'(?i)Engine|Emissions|Horsepower|Travel|Cooling', specname):
                            rob.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "engine")
                        elif re.search(r'(?i)Length|Height|Radius|Track|Width|Load', specname):
                            rob.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "dimensions")
                        elif re.search(r'(?i)Weight|Load', specname):
                            rob.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "weights")
                        elif re.search(r'(?i)Auxiliary|Flow|System|Relief|Pressure', specname):
                            rob.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "hydraulics")
                        else:
                            rob.creat_spec({"specNamel": specname, "metricUnitValue": specvalue}, "operational")
                    else:
                        pass
        else:
            print('Error1')
            # pass
    except BaseException:
        pass

    # getting Images of model
    try:
        images = []
        prefix = 'https://forestriverinc.com'
        pics = s.findAll('img')[7:]
        for link in pics:
            a = link.get('src')
            index = a.find('/I')
            if 'ImageHandler' in a:
                images.append(prefix + a[index:])

        temp_imag = OrderedSet(images)
        # print(temp_imag)

        # put images in json object
        for ImgIndex in temp_imag:
            rob.fetch_img_manual(ImgIndex)
    except BaseException:
        print('ErrorImg')
        pass

    # definitions/ operations
    # try:
    #     definit = s.find('div', id='collapseConOne1').findAll('p')
    #     operat = [p.text.strip() for p in definit]
    #     # print(operat)
    # except:
    #     pass

    # getting videos related to model
    try:
        video = s.find('div', class_='mb-3').find('a').get('href')
        rob.fetch_videos(video)
        print(video)
    except BaseException:
        # print('ErrorV')
        pass

    return rob
    # return model, producturl, temp_imag, specific_name, spacific_value, operat, video

# def distroy():
#     # freed occupied memory
#     fin_robo.destroy()


# Main function start

if __name__ == "__main__":

    URL = "https://forestriverinc.com/search?q=Cedar%20Creek"
    # robot = bot(URL)  # making object of bot class
    river= bot(URL)


    # sending the request to page with parameters
    (soup, code) = river.get_content(URL, {"method": "get", "bs4": "y"})
    clean_links = get_product_url(soup)    # function calling
    # print(clean_links)

    for url2 in clean_links:
        # sending the request to page with parameters
        (soup2, code2) = river.get_content(url2, {"method": "get", "bs4": "y"})
        category, subcat, description, features, options, model_links = general_page_scraping(soup2)
        # (category, subcat, description, features, options, product_links)

        if model_links is not None:
            for model_url in model_links:
                # sending the request to page with parameters
                river.MasterCategory(category)
                river.SubCategory(subcat)
                river.Description(description)
                river.ProductUrl(model_url)
                river.Country("US")
                river.ManufacturerName("Forest River, Inc.")

                TempFeatList = OrderedSet(features)  # features object
                for FetIndex in TempFeatList:
                    river.Features(FetIndex)

                TempOptionList = OrderedSet(options)  # options object
                for OptIndex in TempOptionList:
                    river.Options(OptIndex)

                (sp2, code3) = river.get_content(model_url, {"method": "get", "bs4": "y"})
                river = model_page_scraping(sp2, river)  # change
                # (model, productUrl, images, specname, specvalue, operat, video)

                # try:
                river.make_json()     # creating json file
                # except BaseException:
                #     print('ErrorR')
                #     pass
        else:
            pass

    river.destroy()
