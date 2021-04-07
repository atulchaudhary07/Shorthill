# -*- coding: UTF-8 -*-
import requests,re,os,datetime,os,sys,warnings,hashlib,time,PyPDF2,json,inspect,shutil,io,codecs
warnings.filterwarnings("ignore")
from unidecode import unidecode
from time import sleep
from bs4 import BeautifulSoup
from collections import OrderedDict
import copy
from datetime import datetime,date,time



class bot:
    
    def __init__(self,url):
        self.url = url

        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        self.current_file_name = module.__file__

        self.foldername = re.sub(r'\.py',"",self.current_file_name)
        foldername = self.foldername
        self.header = {'User-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        self.filename = foldername +".json"
        file = open(self.filename,'w+')
        file.close()

        
        self.ObjStr = {
               "_id":None,
                "general":{
                "manufacturer": None,
                "model": None,
                "year": None,
                "msrp": None,
                "category": None,
                "subcategory": None,
                "description": None,
                "countries":None
            
            },
            "images":None,
            "operational":None,
            "engineDriveTrain":None,
            "measurements":None,
            "hydraulics":None,
            "body":None,
            "engine":None,
            "weights":None,
            "electrical":None,
            "battery":None,
            "features":None,
            "options":None,
            "attachments":None,
            "productUri":None,
            "videos":None,
            "dimensions":None,
            "drivetrain":None,
            "other":None

            
        }
        self.objCp = self.ObjStr
        self.ObjectId = ""
        self.product_count = 1
        self.pdf_count = 1
        self.img_count = 1
        self.vid_count = 1


    def get_content(self,url,param,otherHeader=None,cook=None,proxy=None):
                
        try:
            if(param["method"] == "GET" or param["method"] == "get"):
                if(otherHeader is not None and cook is not None and proxy is not None):
                    r = requests.post(url,headers=otherHeader,cookies=cook,proxies=proxy)
                elif(otherHeader is None and cook is not None and proxy is not None):
                    r = requests.post(url,headers=self.header,cookies=cook,proxies=proxy)
                elif(otherHeader is None and cook is None and proxy is not None):
                    r = requests.post(url,headers=self.header,proxies=proxy)

                elif(otherHeader is None and cook is not None):
                    r = requests.post(url,headers=self.header,cookies=cook)
                elif(otherHeader is None):
                    r = requests.get(url, headers=self.header)
                elif("verify" in otherHeader):
                    r = requests.get(url, headers=self.header,verify=otherHeader["verify"])
                else:
                    r = requests.get(url,headers=otherHeader)


            if(param["method"] == "POST" or param["method"] == "post"):
                if("data" in param and otherHeader is not None and cook is not None):
                    r = requests.post(url,data=param["data"], headers=otherHeader,cookies=cook)
                elif("data" in param and otherHeader is None and cook is not None):
                    r = requests.post(url,data=param["data"],headers=self.header,cookies=cook)
                elif("data" in param and otherHeader is not None):
                    r = requests.post(url,data=param["data"],headers=otherHeader)

                else:
                    r = requests.post(url,headers=otherHeader)
            if(r.status_code == 200):
                r.encoding = 'utf-8'
                print("Fetching "+url)
                if(r.status_code == 200):
                    if("bs4" in param and (param["bs4"] == "yes" or param["bs4"] == "y")):
                        return (BeautifulSoup(r.text),r.status_code)
                    elif("json" in param and (param["json"] == "yes" or param["json"] == "y")):
                        return (json.loads(r.text),r.status_code)
                    else:
                        return (r.text,r.status_code)

                else:
                    r.delete
                    return ("Error",r.status_code)
        except TypeError as e:
            print(e)  

    def create_md5(self,url):
        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        #m.update(url)
        return m.hexdigest()

    def special_charCare(self,value):
        if(value is None):
            return ""
        value = str(value)
        value = re.sub(r'^[\s\t]+',"",value)
        if(re.search(r'^\s*$',value)):
            return ''
        value = re.sub(r'[\s\t]+'," ",value)
        value=re.sub(r'\\\\x[a-z0-9]{2}',"",value)
        value=re.sub(r'\\\\\w+\s',"",value)
        value = unidecode(value)
        value = value.encode("unicode_escape") 
        value = value.decode("utf-8")
        value = re.sub(r'\\\\\"','\"',value)
        value = re.sub(r'<[^>]+>'," ",value)
        value = re.sub(r'\\+[nrtx]|\n\t\r\t',' ',value)
        if(re.search(r'^\s*[:\-\s\t\| ]+.*s\w+',value)):
            value = re.sub(r'^\s*[:\-\s\t\| ]+','',value)
        value = re.sub(r'\s+$','',value)
        return value

    def ObjectID(self,model):
        self.ObjectId = self.create_md5(model)
        self.ObjStr["_id"] = self.ObjectId
        self.ObjStr["general"]["year"] = 2021
        if self.ObjStr["general"]["msrp"] is None:
            self.ObjStr["general"]["msrp"] = 0.0
       
        if(re.search(r'\w',model)):
            self.ObjStr["general"]["model"] = model
        self.pdf_count = 1
        self.img_count = 1
        self.vid_count = 1

    def ProductUrl(self,uri):
        self.ObjStr["productUri"] = uri

    def ManufacturerName(self,manufacturer):
        manufacturer = self.special_charCare(manufacturer)
        if(re.search(r'\w',manufacturer)):
            self.ObjStr["general"]["manufacturer"] = manufacturer
    
    def Country(self,country):
        country = self.special_charCare(country)
        if(self.ObjStr["general"]["countries"] is None): self.ObjStr["general"]["countries"] = []
        if(re.search(r'\w',country)):
            self.ObjStr["general"]["countries"].append(country)
    
    def MasterCategory(self,category):
        category = self.special_charCare(category)
        if(re.search(r'\w',category)):
            self.ObjStr["general"]["category"] = category

    def SubCategory(self,subcategory):
        subcategory = self.special_charCare(subcategory)
        if(re.search(r'\w',subcategory)):
            self.ObjStr["general"]["subcategory"] = subcategory
        
        
    def Title(self,title):
        title = self.special_charCare(title)
        return title
      

    def Options(self,option):
        option = self.special_charCare(option)
        if re.search(r'\w',option):
            if(self.ObjStr["options"] is None): self.ObjStr["options"]  = []
            if(re.search(r'\w',option)):
                self.ObjStr["options"].append(option)

    def Features(self,features):
        features = self.special_charCare(features)
        if re.search(r'\w',features):
            if(self.ObjStr["features"] is None): self.ObjStr["features"]  = []
            if(re.search(r'\w',features)):
                self.ObjStr["features"].append(features)

    def Year(self,yer):
        self.ObjStr["general"]["year"] = yer


    def Msrp(self,msrp):
       
        msrp = self.special_charCare(msrp)
        if(re.search(r'\w',msrp)):
            msrp = re.sub(r'[^\d\.]+',"",msrp)
            self.ObjStr["general"]["msrp"] = float(msrp)

    
    def Description(self,description):
        description = self.special_charCare(description)
        if(re.search(r'\w',description)):
            self.ObjStr["general"]["description"] = description

    def allDir(self,getname):
        try: 
            os.makedirs(getname)
        except OSError:
            if not os.path.isdir(getname):
                raise

    def download_bs64(self,url,filepath):
        try:
            r = requests.get(url, stream=True)
            with open(filepath, 'wb') as fd:
                chunk_size = 2000
                for chunk in r.iter_content(chunk_size):
                    fd.write(chunk)
        except requests.exceptions.RequestException as e:
            print(e)

    def fetch_img_manual(self,imageURL,imageName=None,imgDesc=None):
        print("Downloading images")
       
   
        if imageName is not None:
            imageName = self.special_charCare(imageName)
            if(re.search(r'^\s*$',imageName)):
                imageName = None

        if(imgDesc is not None):
            imgDesc = self.special_charCare(imgDesc)
            if(re.search(r'^\s*$',imgDesc)):
                imgDesc = None

        if(self.ObjStr["images"] is None): self.ObjStr["images"]  = []
        new_obj ={
        "src" : imageURL,
        "desc" : imageName,
        "longDesc" : imgDesc,
        # "imageId":image_id
        }
        self.ObjStr["images"].append(new_obj)
        self.img_count+=1

    def fetch_pdf_manual(self,j,pdfnm=None,pdfdesc=None):
        ObjectID = self.ObjectId
      
        pdfnm = self.special_charCare(pdfnm)
        if re.search(r'^\s*$',pdfnm):
            pdfnm = None

        if(pdfdesc is not None):
            pdfdesc = self.special_charCare(pdfdesc)
            if(re.search(r'^\s*$',pdfdesc)):
                pdfdesc = None
        pdfdesc = "product_brochure"

        myObj = {
            "attachmentDescription":pdfnm,                  
            "attachmentLocation":j,
            "attachmentDescription":pdfdesc
            
            
        }
        if(self.ObjStr["attachments"] is None): self.ObjStr["attachments"]  = []
        self.ObjStr["attachments"].append(myObj)
        self.pdf_count+=1


    def fetch_img(self,img_cont,attr):
            img_json = ""

            print("Downloading images")
            for img_ech in img_cont.find_all(attr["tagname"]):
                sys.stdout.write(str(self.img_count))
                sys.stdout.flush()
                sys.stdout.write('\b\b\b')
                imageURL = img_ech.get(attr["attrURL"])
                if(imageURL is None):
                    continue
                if(re.search(r'^(\.\.\/)+',imageURL)):
                    imageURL=re.sub(r'^(\.\.\/)+','',imageURL)
                    imageURL = self.url+imageURL
                elif(re.search(r'^\/\/',imageURL)):
                    imageURL = "http:"+imageURL
                elif(re.search(r'^http',imageURL)):
                    imageURL = imageURL
                else:
                    imageURL = self.url+imageURL
                imageName = None
                if(img_ech.get(attr["attrName"]) is not None):
                    imageName = img_ech.get(attr["attrName"])

                imageName = self.special_charCare(imageName)
                if 'youtu' in imageURL.lower():
                    continue
                if(re.search(r'^\s*$',imageName)):
                    imageName = None
                if(self.ObjStr["images"] is None): self.ObjStr["images"]  = []
                new_obj ={
                "src" : imageURL,
                "desc" : imageName,
                "longDesc" : None,
            
                }
                self.ObjStr["images"].append(new_obj)
                self.img_count+=1
                print("")
            return img_json.strip().rstrip(",")
        


    def fetch_pdf(self,pdf_cont):
        ObjectID = self.ObjectId
        pdfobj = {}
        print("Downloading pdf")
        # count_product = 1
        
        for ech_pdf in pdf_cont.find_all("a",{"href":re.compile(r".+\.pdf|\.PDF")}):
            hrf = ech_pdf.get("href")
            if(re.search(r'^(\.\.\/)+',hrf)):
                hrf=re.sub(r'^(\.\.\/)+','',hrf)
                hrf = self.url+hrf
            elif(re.search(r'^\/\/',hrf)):
                hrf = "http:"+hrf
            elif(re.search(r'^http',hrf)):
                hrf = hrf
            else:
                hrf = self.url+hrf
            pdfobj[hrf] = ech_pdf.getText().strip()
    
        abcd = 1
        for j in pdfobj:
            sys.stdout.write(str(self.pdf_count))
            sys.stdout.flush()
            sys.stdout.write('\b\b\b')
            pdfnm = self.special_charCare(pdfobj[j])
            if re.search(r'^\s*$',pdfnm):
                pdfnm = None
            myObj = {
               
                "attachmentDescription":"product_brochure_"+str(abcd),
                "attachmentLocation":j,
               
            }
            abcd=abcd+1
            if(self.ObjStr["attachments"] is None): self.ObjStr["attachments"]  = []
            self.ObjStr["attachments"].append(myObj)
            self.pdf_count+=1


    def fetch_videos(self,vidUrl,vidname=None,vidDesc=None):
        if '.jpg' in vidUrl.lower():
            pass
        else:
            if(vidDesc is not None):
                vidDesc = self.special_charCare(vidDesc)
                if(re.search(r'^\s*$',vidDesc)):
                    vidDesc = None        
            print("Downloading video links")
            # vid_id=self.ObjectId+"_"+str(self.vid_count)
            vidname = "video"
            myObj ={
           "src" : vidUrl
            }
            if(self.ObjStr["videos"] is None): self.ObjStr["videos"]  = []
            self.ObjStr["videos"].append(myObj)
            self.pdf_count+=1


    def excp_handle(self,val1,val2,val3):
        #Caution: this is only for find not for findall
        if(val1.find(val2,val3) is not None):
            vm = val1.find(val2,val3).getText().strip()
            vm = re.sub(r'\s+'," ",vm)
            return  re.sub(r'"','\\"',vm)
        else:
            return ""

    def capitalizeWords(self,s):
        m =  re.sub(r'\w+', lambda m:m.group(0).capitalize(), s)
        m =  re.sub(r'\W',"",m)
        m =  re.sub(r'^(.)', lambda m:m.group(0).lower(), m)
        return m

    def camelCase(self,m):
        s=m.split(" ")
        s= [x.title() for x in s]
        s[0]=s[0].lower()
        s = "".join(s)
        s =re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", s)
        s = re.sub('[^A-Za-z0-9]+', '', s)

        return s


    def creat_spec(self,args,spectype):
        specName1 = self.capitalizeWords(args["specNamel"])
        spec_Name2 = self.special_charCare(args["specNamel"])
        specName1 = self.special_charCare(specName1)
        value = self.special_charCare(args["metricUnitValue"])
        value = re.sub(r'^\s*:','',value)
        if re.search(r'^\s*$',specName1):
            return
        if re.search(r'^\s*$',value):
            value = None
        newObj = {self.camelCase(spec_Name2):{"label":spec_Name2,"desc":value}}
        if("engine" in spectype or "Engine" in spectype or "e" == spectype):
            if(self.ObjStr["engineDriveTrain"] is None): self.ObjStr["engineDriveTrain"]  = {}
            self.ObjStr["engineDriveTrain"].update(newObj)
        
        elif("operation" in spectype or "Operation" in spectype or "o" == spectype or "operational" in spectype):
            if(self.ObjStr["operational"] is None): self.ObjStr["operational"]  = {}
            self.ObjStr["operational"].update(newObj)
        
        elif("body" in spectype or "body" in spectype or "body" == spectype):
            if(self.ObjStr["body"] is None): self.ObjStr["body"]  = {}
            self.ObjStr["body"].update(newObj)
        elif("hydraulics" in spectype or "hydraulics" in spectype or "hydraulics" == spectype):
            if(self.ObjStr["hydraulics"] is None): self.ObjStr["hydraulics"]  = {}
            self.ObjStr["hydraulics"].update(newObj)
        elif("measurements" in spectype or "measurements" in spectype or "measurements" == spectype):
            if(self.ObjStr["measurements"] is None): self.ObjStr["measurements"]  = {}
            self.ObjStr["measurements"].update(newObj)
        elif("electrical" in spectype or "electrical" in spectype or "electrical" == spectype):
            if(self.ObjStr["electrical"] is None): self.ObjStr["electrical"]  = {}
            self.ObjStr["electrical"].update(newObj)
        elif("drivetrain" in spectype or "drivetrain" in spectype or "drivetrain" == spectype):
            if(self.ObjStr["drivetrain"] is None): self.ObjStr["drivetrain"]  = {}
            self.ObjStr["drivetrain"].update(newObj)
        elif("weights" in spectype or "weights" in spectype or "w" == spectype):
            if(self.ObjStr["weights"] is None): self.ObjStr["weights"]  = {}
            self.ObjStr["weights"].update(newObj)
        elif("dimensions" in spectype or "dimensions" in spectype or "d" == spectype):
            if(self.ObjStr["dimensions"] is None): self.ObjStr["dimensions"]  = {}
            self.ObjStr["dimensions"].update(newObj)
        else:
            if(self.ObjStr["other"] is None): self.ObjStr["other"]  = {}
            self.ObjStr["other"].update(newObj)


    def remove_null_nodes(self):
        a = copy.deepcopy(self.ObjStr)
        for i in a:
            if a[i] is None:
                print (i)
                del (self.ObjStr[i])

            if i == "general"and a[i]  is not None:

                general={
                    "manufacturer": None,
                    "model": None,
                    "year": None,
                    "msrp": None,
                    "category": None,
                    "subcategory": None,
                    "description": None,
                    "countries":None
            
                
                }
                general_node = a["general"]
                if general_node["description"] is None:
                    general["description"]=""
                    general["manufacturer"]=a["general"]["manufacturer"]
                    general["model"]=a["general"]["model"]
                    general["year"]=a["general"]["year"]
                    general["msrp"]=a["general"]["msrp"]
                    general["category"]=a["general"]["category"]
                    general["subcategory"]=a["general"]["subcategory"]
                    general["countries"]=a["general"]["countries"]

                    self.ObjStr['general'] = general


                
            if i == 'images' and a[i] is not None:
                new_image_list = []
                for j in a['images']:
                    img_dict = {
                        'src' :None,
                        'desc' : None,
                        'longDesc' : None
                    }

                    if j['src'] is not None:
                        img_dict['src'] = j['src']
                    else:
                        del(img_dict['src'])

                    if j['desc'] is not None:
                        img_dict['desc'] = j['desc']
                    else:
                        del(img_dict['desc']) 

                    if j ['longDesc'] is not None:
                        img_dict['longDesc'] = j ['longDesc']
                    else:
                        del(img_dict['longDesc'])

                    new_image_list.append(img_dict)
                self.ObjStr['images'] = new_image_list

            if i == 'attachments' and a[i] is not None:
                new_attchment_list = []
                x=1
                for j in a['attachments']:
                    attachment_dict = {
                        'attachmentDescription' :None,
                        'attachmentLocation' : None,
                        
                    }

                    if j['attachmentDescription'] is not None:
                        attachment_dict['attachmentDescription'] = j['attachmentDescription']
                    else:
                        attachment_dict['attachmentDescription'] = "Product_"+str(x)

                    if j['attachmentLocation'] is not None:
                        attachment_dict['attachmentLocation'] = j['attachmentLocation']
                    else:
                        attachment_dict['attachmentLocation'] = ""
                    x=x+1

                    

                    new_attchment_list .append(attachment_dict)
                self.ObjStr['attachments'] = new_attchment_list
                
        
        
    def make_json(self):

        if(self.ObjStr["productUri"] is None):
            print("\n\nError:\nProductUrl should not be None\nScript Ending")
            sys.exit()

        if(self.ObjStr["_id"] is None):
            print("\n\nError:\nObjectID should not be None\nScript Ending")
            sys.exit()

        if(self.ObjStr["general"]["manufacturer"] is None):
            print("\n\nError:\nManufacturerName should not be None\nScript Ending")
            sys.exit()

        if(self.ObjStr["general"]["countries"] is None):
            print("\n\nError:\nCountry should not be None\nScript Ending")
            sys.exit()

        if(self.ObjStr["general"]["category"] is None):
            print("\n\nError:\n Category should not be None\nScript Ending")
            sys.exit()

        with io.open(self.filename, 'a+',encoding="utf8") as json_file:
            if(self.product_count == 1):
                json_file.write("[")
            self.remove_null_nodes()
            #{k: v for k, v in metadata.items() if v is not None}

            data = json.dumps(self.ObjStr, sort_keys=False,indent=4, ensure_ascii=False)
            json_file.write(str(data))
            json_file.write(",")
        self.product_count+=1



        
        self.ObjStr = {
            "_id":None,
            "general":{
                "manufacturer":None ,
                "model": None,
                "year": None,
                "msrp": None,
                "category": None,
                "subcategory": None,
                "description": None,
                "countries":None
                # "extractedDate":None,
            },
            
            "images":None,
            "operational":None,
            "engineDriveTrain":None,
            "measurements":None,
            "hydraulics":None,
            "body":None,
            "engine":None,
            "weights":None,
            "electrical":None,
            "battery":None,
            "features":None,
            "options":None,
            "attachments":None,
            "productUri":None,
            "videos":None,
            "dimensions":None,
            "drivetrain":None,
            "other":None

        }


    def pdf_read(self,filename):
        pdfFileObj = open(self.foldername+"/pdf/"+filename,'rb')     #'rb' for read binary mode
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pdfReader.numPages
        pageObj = pdfReader.getPage(0)          #'9' is the page number
        m = pageObj.extractText().encode()
        return (str(m))
    
    
    def destroy(self):

        with open(self.filename, 'rb+') as filehandle:
            filehandle.seek(-1, os.SEEK_END)
            filehandle.truncate()
        with open(self.filename, 'a+') as filehandle:
            filehandle.write("]")
        # shutil.copy2(self.current_file_name, self.foldername)
        print("Total product count "+str(self.product_count))
        print("\a\a\a\a")

        

        json_data=open(self.filename,encoding='utf-8')
        data = json.load(json_data)
        for i in data:
            try:
                if i['attachments'] is None:
                    pass
                else:
                    count = 1
                    count1 = 1
                
                    for j in i['attachments']:
                        if(re.search(r'(?i)product_brochure',j['attachmentDescription'])):
                           j['attachmentDescription'] = "product_brochure_"+str(count)
                           count = count+1
            except:
                pass
        json_data.close()
        with open(self.filename, 'rb+') as filehandle:
            filehandle.seek(-1, os.SEEK_END)
            filehandle.truncate()
        foldername = re.sub(r'\.py',"",self.current_file_name)
        last_update = date.today()
        new_file = foldername+str(last_update)+".json"
        with open(new_file, 'w+') as filehandle:
            data = json.dumps(data, sort_keys=False,indent=4, ensure_ascii=False)
            filehandle.write(str(data))
        os.remove(self.filename)

