import requests,sys,csv,traceback,re,json,os
from bs4 import BeautifulSoup
from random import random,shuffle
from time import sleep

delay_base = 0.2    # time to wait between requests
delay_noise = 0.1
zipcode = 61821
cacheDir = "./json_cache"


### Kelly Blue Book ######################

def kbbExtractJson(html):
    soup = BeautifulSoup(html, "lxml")
    jssearch = soup.find(name='script', attrs={'language' : 'javascript'})
    if jssearch:
        code = jssearch.text
    else:
        open("nojs.html", "w").write(html)
        raise RuntimeError

    js = code[code.find("data"):]
    js = js[js.find("{"):]
    bc = 0
    idx = 0
    for c in js:
        if bc == 0 and idx>0: break
        if c=="{": bc +=1
        if c=="}": bc -= 1
        idx+=1
    else:
        raise RuntimeError("bc={}".format(bc))

    jsonstr = js[:idx]

    return json.loads(jsonstr)


def kbbGetData(sess, make,model,year):
    kbbdata = dict()
    kbbCacheFile = "{}/{}-{}-{}_kbb.json".format(cacheDir,make,model,year)
    if os.path.isfile(kbbCacheFile):
        kbbdata = json.load(open(kbbCacheFile))
    else:
        kbbdata = getKbbData(sess, make,model,year)
        json.dump(kbbdata, open(kbbCacheFile, "w"))

    return kbbdata


def kbbBaseUrl(make,model,year):
    mk = make.lower().replace(' ', '-')
    md = model.lower().replace(' ', '-')
    yr = year.lower().replace(' ', '-')
    return "http://www.kbb.com/{make:}/{model:}/{year:}-{make:}-{model:}".format(make=mk,model=md,year=yr)


def kbbCarUrl(make,model,year,trim):
    b = kbbBaseUrl(make,model,year)
    return b + "/{}?condition=good&intent=buy-used&pricetype=retail&persistedcondition=good".format(trim)


def kbbBodytypeUrl(make,model,year):
    b = kbbBaseUrl(make,model,year)
    return b + "/categories/?intent=buy-used"


def kbbTrimUrl(make,model,year, body):
    b = kbbBaseUrl(make,model,year)
    return b + "/styles/?intent=buy-used&bodystyle={}".format(body)


def getKbbData(make,model,year):
    # 1.) get body types
    html, session = getHtml(kbbBodytypeUrl(make,model,year),
                           cookies=dict(ZipCode=str(zipcode),PersistentZipCode=str(zipcode)))

    re_bodystyle = re.compile(r'bodystyle=([^"\'?]+)')
    bodytypes = list(set(re_bodystyle.findall(html)))

    # 2.) get all trims
    trims = set()

    for b in bodytypes:
        html, session = getHtml(kbbTrimUrl(make,model,year,b), session)
        soup = BeautifulSoup(html, "lxml")

        vs = soup.find_all(text='Choose this style')

        for v in vs:
            href = v.parent.attrs['href']
            trim = href.split('/')[4]
            trims.add(trim)

    # 3.) scrape data for each trim
    scraped = dict()
    for t in trims:
        html, session = getHtml(kbbCarUrl(make,model,year,t), session)
        jd = kbbExtractJson(html)
        scraped[t] = jd['values']

    return scraped


### JD Power & Assoc. ####################

def jdpSearchUrl(make,model,year):
    mk = make.replace(' ', '+')
    md = model.replace(' ', '+')
    return "http://autos.jdpower.com/research/{}/index.htm?modelGroup={}&sortBy=year%20desc&year={}".format(make,model,year)


def jdpGetRatingsUrlAndMPG(make, model, year):
    html, _ = getHtml(jdpSearchUrl(make,model,year))
    soup = BeautifulSoup(html, "lxml")
    sresults = soup.findAll('li', attrs={'class':'ddc-unit'})
    rem = re.compile("research")
    us = []
    re_mpg = re.compile("Hwy (\d+)/City (\d+)")
    for sr in sresults:
        mpg_str = sr.find(text=lambda x: "Hwy" in x)
        mpg_hwy, mpg_city = re_mpg.findall(mpg_str)[0]
        u = sr.find('a',attrs={'href':rem}).attrs['href']
        u1 = "http://autos.jdpower.com" + '/'.join(u.split('/')[:-1]) + "/ratings.htm"
        us.append(u1)

    if len(us) == 0:
        raise RuntimeError("no matches")

    return us[0], float(mpg_hwy), float(mpg_city)


def jdpScrapeRatings(html):
    soup = BeautifulSoup(html,"lxml")
    elems = soup.findAll(attrs={"itemprop":"ratingValue"})
    r = dict()
    for elem in elems:
       val = float(elem.getText())
       key = elem.parent.parent.findAll('span')[0].getText()
       r[key] = val
   
    return r


def jdpGetData(make,model,year):
    jsonCacheFile = "{}/{}-{}-{}_jdp.json".format(cacheDir,make,model,year)
    if os.path.isfile(jsonCacheFile):
        rts=json.load(open(jsonCacheFile))
    else:
        ratings_url, mpg_hwy, mpg_city = jdpGetRatingsUrlAndMPG(make,model,year)
        html, _ = getHtml(ratings_url)
        rts = jdpScrapeRatings(html)
        rts['mpgCity'] = mpg_city
        rts['mpgHwy'] = mpg_hwy
        json.dump(rts, open(jsonCacheFile, "w"))

    return rts


##########################################

def getHtml(url, sess=None, cookies=None):
    if not sess:
        sess = requests.Session()

    sleep(delay_base + delay_noise*random())
    req = sess.get(url,cookies=cookies)
    html = req.content.decode()
    if not req.ok:
        open("error.html","w").write(html)
        raise RuntimeError("{} {}: {}".format(req.status_code, req.reason, url))

    open("current.html","w").write(html)

    return html,sess


if __name__ == '__main__':
    try:
        inputCsvFile = sys.argv[1]
        outputJsonFile = sys.argv[2]
    except:
        print("usage: {} input.csv output.json".format(sys.argv[0]))
        sys.exit(1)

    try:
        os.mkdir(cacheDir)
    except:
        pass
    
    cars = list(csv.reader(open(inputCsvFile)))
    shuffle(cars)
    cardata = dict()

    for year,make,model in cars:
        try:
            car = "{} / {} / {}".format(make,model,year)
            cardata[car] = dict(ratings=jdpGetData(make,model,year),
                                pricing=getKbbData(make,model,year))
            print("{} - {} - {}".format(make, model, year))

            json.dump(cardata, open(outputJsonFile, "w"), indent=3)
        except:
            e,v,t = sys.exc_info()
            if e == KeyboardInterrupt or e == SystemExit:
                sys.exit()

            print()
            print("*"*80)
            print (" === {} - {} - {} ===".format(make,model,year))
            traceback.print_exc()
            print("*"*80)
            print()

