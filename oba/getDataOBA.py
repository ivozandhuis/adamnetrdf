#! /usr/bin/env python3

import urllib
import rdflib
from bs4 import BeautifulSoup

oba = rdflib.Graph()
kb  = rdflib.Graph()
dc  = rdflib.Namespace("http://purl.org/dc/elements/1.1/")
edm = rdflib.Namespace("http://www.europeana.eu/schemas/edm/")

oba.bind("dc", dc)
oba.bind("edm", edm)


pages = 1
errorlist = [] # contains all non-available uri's on data.bibliotheken.nl

for p in range(1, pages+1):
    requestUrl = "http://obaliquid.staging.aquabrowser.nl/api/v0/search/?q=amsterdam&authorization=2edf326f3037fb1b0d40867c43eaa108&page=" + str(p)
    print(requestUrl) # debugging & progress
    reply = urllib.request.urlopen(requestUrl)
    soup = BeautifulSoup(reply, "lxml")
    results = soup.find_all("result")

    for result in results:

        # get data from response
        ppns       = result.find_all("ppn-id")
        identifier = result.find("id")
        subjects   = result.find_all("topical-subject")

        if identifier.text.startswith("|oba-catalogus|"): # check for publications in catalogue only
            for ppn in ppns: # iterate through available ppn's
                uri = "http://data.bibliotheken.nl/doc/nbt/p" + ppn.text
                b = rdflib.Graph()
                result = b.parse(uri)

                if len(b) > 0: # check if PPN uri exists
                    kb = kb + b
                    book = rdflib.URIRef(uri)
                    url  = "https://zoeken.oba.nl/detail/?itemid=" + urllib.parse.quote(identifier.text)
                    url  = rdflib.URIRef(url)
                    oba.add( (book, dc.type, rdflib.Literal("book")) )
                    oba.add( (book, dc.identifier, rdflib.Literal(identifier.text)) )
                    oba.add( (book, edm.isShownAt, url) )

                    for subject in subjects:
                        oba.add( (book, dc.subject, rdflib.Literal(subject.text)) )

                else: # if PPN uri does nog exist
                    errorlist.append(uri)

# serialize and write to file
s = oba.serialize(format='turtle')
file = open("OBAcatalogus.ttl","wb")
file.write(s)
file.close()

# serialize and write to file
s = kb.serialize(format='turtle')
file = open("NBTinOBA.ttl","wb")
file.write(s)
file.close()
