#! /usr/bin/env python3

import urllib.request
import rdflib
from bs4 import BeautifulSoup

streets = {
"Pijp" : "https://adamlink.nl/geo/TODO",
"Sint Antoniebreestraat" : "https://adamlink.nl/geo/street/sint-antoniesbreestraat/4096",
"Kalverstraat" : "https://adamlink.nl/geo/street/kalverstraat/2269",
"Rokin" : "https://adamlink.nl/geo/street/rokin/3867",
"Dam" : "https://adamlink.nl/geo/street/dam/880"
}

g = rdflib.Graph()

print("@prefix dcterms: <http://purl.org/dc/terms/> .")
print("@prefix owl: <http://www.w3.org/2002/07/owl#> .")
print("@prefix edm: <http://www.europeana.eu/schemas/edm/> .")


for street in streets:
    streetterm = street.replace(" ", "%20")
    requestUrl = "http://obaliquid.staging.aquabrowser.nl/api/v1/search/?q=amsterdam%20" + streetterm + "&authorization=2edf326f3037fb1b0d40867c43eaa108"
    reply = urllib.request.urlopen(requestUrl)
    soup = BeautifulSoup(reply, "lxml")

    c = soup.find("count")
    count = int(c.text)
    pages = int(count/20) + 1
#    print(street + " " + str(count) + " hits en " + str(pages) + " pages.") # debuging

    for p in range(1, pages+1):
        requestUrl = "http://obaliquid.staging.aquabrowser.nl/api/v1/search/?q=amsterdam%20" + streetterm + "&page=" + str(p) + "&authorization=2edf326f3037fb1b0d40867c43eaa108"
#        print(requestUrl) # debuging
        reply = urllib.request.urlopen(requestUrl)
        soup = BeautifulSoup(reply, "lxml")

        results = soup.find_all("result")

        for result in results:
            identifier = result.find("id")
            ppns       = result.find_all("ppn-id")
            subjects   = result.find_all("topical-subject")

            obacat = identifier.text.startswith("|oba-catalogus|")

            opnemen = 0
            for x in subjects:
                if x.text.startswith(street + " (Amsterdam)"):
                    opnemen = 1

# uri: pipe escapen
            if obacat and opnemen:
                print("<https://zoeken.oba.nl/detail/?itemid=" + identifier.text + ">")
                for ppn in ppns:
                    uri = "http://lod.kb.nl/ppn/" + ppn.text
                    result = g.parse(uri)
                    if len(g)>0:
                        print("   owl:sameAs <" + uri + ">;")
                print("   edm:isShownAt <https://zoeken.oba.nl/detail/?itemid="+identifier.text+">;")
                print("   dcterms:spatial <" + streets[street] + ">.")
