import requests
import json
import datetime
import sys
import os.path
from requests_html import HTMLSession
import json

session = HTMLSession()

def scrape_ad_html(adid):
    r = session.get('https://www.finn.no/realestate/homes/ad.html?finnkode=98344182')

    data = {"properties": {}, "description": {}}
    for element in r.html.find("*[data-automation-id=key],*[data-automation-id=value]"):
        if element.find("*[data-automation-id=key]"):
            key = element.text
        else:
            if element.element.tag == 'dd':
                data["properties"][key] = element.text.replace("\u00a0", " ")
            elif element.element.tag == 'ul':
                data["properties"][key] = [item.text for item in element.find("li")]
            else:
                data["description"][key] = element.html

    for id in ("#matrikkelinfo", "#omkostninger"):
        element = r.html.find(id)[0]
        data["description"][element.find("* > h2")[0].text] = ''.join(e.html for e in element.find("* > :not(h2)"))

    data["description"]["Felleskostnader inkluderer"] = ''.join(
        e.html for e
        in r.html.xpath(
            '//*[h2[contains(.,"Felleskostnader inkluderer")]]'
        )[0].find("* > *:not(h2)")
    )
    return data


name = sys.argv[1]
if sys.argv[2:]:
    date = sys.argv[2]
else:
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    print("Date: %s" % date)

with open("%s.json" % name) as f:
    args = json.load(f)

filename = '%s.map.%s.json' % (name, date)
if os.path.exists(filename):
   with open(filename) as f:
       mapentries = json.load(f)
else:
    print("Downloading map")
    r = requests.post("https://kart.finn.no/ajax.jsf", data=args)
    mapentries = json.loads(r.text)
    with open(filename, 'w') as f:
        json.dump(mapentries, f)

for poi in mapentries["pois"].values():
    for adid in poi["ids"]:
        filename = '%s.ad.%s.poi.json' % (name, adid)
        if not os.path.exists(filename):
            print("Downloading short info for ad %s" % adid)
            r = requests.get("https://kart.finn.no/map/object/group/content/%s.json" % adid)
            addata = json.loads(r.text)
            with open(filename, 'w') as f:
                json.dump(addata, f)
        filename = '%s.ad.%s.parsed.json' % (name, adid)
        if not os.path.exists(filename):
            print("Downloading long info for ad %s" % adid)
            addata = scrape_ad_html(adid)
            with open(filename, 'w') as f:
                json.dump(addata, f)

    
# https://www.finn.no/realestate/homes/ad.html?finnkode=123075082
