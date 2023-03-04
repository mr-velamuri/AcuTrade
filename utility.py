import requests
import json
import math
import sys


with open('AcuAnalysisDB.json', 'r', encoding='utf-8') as openfile:
    try:
        # Reading from json file
        dbData = json.load(openfile)
        #dbData = openfile.readlines()
        print("in Try")
    except:
        with open('OriginalDB.json', 'r', encoding='utf-8') as openfile:
            dbData = json.load(openfile)
            print("In Except")
                
    #print(dbData)

index_obj = dict()
oi_obj = dict()

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'}

sess = requests.Session()
cookies = dict()

def print_hr():
    print(("|".rjust(70,"-")))

def set_cookie():
    request = sess.get(dbData["urls"]["url_oc"], headers=headers, timeout=5)
    cookies = dict(request.cookies)
  
def get_data(url):
    set_cookie()
    response = sess.get(url, headers=headers, cookies=cookies)
    if(response.status_code==401):
        set_cookie()
        response = sess.get(url, headers=headers, cookies=cookies)
        print("Error in fetching data from " + url)
    if(response.status_code==200):
        return response.text
    return ""

def get_index_stats(symbol = "NIFTY"):
    response_text = get_data(dbData["urls"]["equity_url"]+str(dbData["symbols"][symbol]["SI"]))
    data = json.loads(response_text)
        
    dbData["thisProps"][symbol]["dayOpen"] = data["data"][0]["open"]
    dbData["thisProps"][symbol]["time-series"]["dayHigh"].append(data["data"][0]["dayHigh"])
    dbData["thisProps"][symbol]["time-series"]["dayLow"].append(data["data"][0]["dayLow"])
    dbData["thisProps"][symbol]["time-series"]["dayCurrent"].append(data["data"][0]["lastPrice"])
    dbData["thisProps"][symbol]["time-series"]["pChange"].append(data["data"][0]["pChange"])
    dbData["thisProps"][symbol]["advances"] = data["advance"]["advances"]
    dbData["thisProps"][symbol]["declines"] = data["advance"]["declines"]
    dbData["thisProps"][symbol]["unchanged"] = data["advance"]["unchanged"]
    
    #print(json.dumps(dbData["thisProps"], indent = 2))
    return ""

def print_adv_dec(symbol = "NIFTY"):
    if(dbData["thisProps"][symbol]["advances"] == 0):
       return "First Data Load cheyyara pandi"
    adv = int(dbData["thisProps"][symbol]["advances"])
    decl = int(dbData["thisProps"][symbol]["declines"])
    uchgd = int(dbData["thisProps"][symbol]["unchanged"])
    tot = adv + decl + uchgd

    adv_per = round((adv/tot)*100)
    decl_per = round((decl/tot)*100)
    print("Arey Rammi ga")
    
    if(abs(adv_per - decl_per) <= 10):
        return symbol + " - Sideways ra babu.. light thesuko"
    elif(abs(adv_per - decl_per) > 10 and abs(adv_per - decl_per) <= 30):
        return symbol + " - Ide trend continue avvochu"
    elif(adv_per >= 70):
        return symbol + " - Bhayankaramaina up move ra babu"
    elif(decl_per >= 70):
        return symbol + " - Bhayankaramaina down move ra babu"
    else:
        return symbol + " - Not Sure.. Go to Hell"