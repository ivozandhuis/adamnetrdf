#! /usr/bin/env python3

import urllib
import rdflib
from bs4 import BeautifulSoup
import csv

# You'll need an authorization to use the API ...
key = "your_key_here"

oba = rdflib.Graph()
nbt  = rdflib.Graph()

dc   = rdflib.Namespace("http://purl.org/dc/elements/1.1/")
edm  = rdflib.Namespace("http://www.europeana.eu/schemas/edm/")
foaf = rdflib.Namespace("http://xmlns.com/foaf/0.1/")

oba.bind("dc", dc)
oba.bind("edm", edm)
oba.bind("foaf", foaf)

pages = 1000

# set up outputfile in csv-format for non-existent PPN's
outfile = open('errors.csv', 'w', newline='')
fieldnames = ['uri', 'url', 'error']
errors = csv.DictWriter(outfile, fieldnames=fieldnames)
errors.writeheader()

for p in range(500, pages+1):
    requestUrl = "http://obaliquid.staging.aquabrowser.nl/api/v0/search/" + \
        "?q=amsterdam" + \
        "&authorization=" + key + \
        "&page=" + str(p)
    print(requestUrl) # debugging & progress
    reply = urllib.request.urlopen(requestUrl)
    soup = BeautifulSoup(reply, "lxml")
    results = soup.find_all("result")

    for result in results:

        # get data from response
        ppns       = result.find_all("ppn-id")
        identifier = result.find("id")
        subjects   = result.find_all("topical-subject")
        summaries  = result.find_all("summary")

        # check for publications in catalogue only
        if identifier.text.startswith("|oba-catalogus|"):

            for ppn in ppns: # iterate through available ppn's
                url  = "https://zoeken.oba.nl/detail/?itemid=" + \
                    urllib.parse.quote(identifier.text)
                uri = "http://data.bibliotheken.nl/id/nbt/p" + ppn.text
                pic = "https://cover.biblion.nl/coverlist.dll" + \
                    "?bibliotheek=oba&ppn=" + ppn.text

                print(uri) # debugging & progress

                # check if PPN uri exists
                b = rdflib.Graph()
                error = {}
                try:
                    r = b.parse(uri)
                except Exception as e:
                    error['error'] = e
                    error['url'] = url
                    error['uri'] = uri
                    errors.writerow(error)

                if len(b) > 0: # mostly: no errors, but no graph either ...
                    nbt = nbt + b
                    book = rdflib.URIRef(uri)
                    url  = rdflib.URIRef(url)
                    pic  = rdflib.URIRef(pic)

                    oba.add( (book, dc.identifier, rdflib.Literal(identifier.text)) )
                    oba.add( (book, edm.isShownAt, url) )
                    oba.add( (book, foaf.depiction, pic) )

                    for subject in subjects:
                        oba.add( (book, dc.subject, rdflib.Literal(subject.text)) )

                    for summary in summaries:
                        oba.add( (book, dc.description, rdflib.Literal(summary.text)) )

                else: # if no error was thrown, but graph was empty
                    error['error'] = "empty graph"
                    error['url'] = url
                    error['uri'] = uri
                    errors.writerow(error)

    # write every x pages into a file
    x = 50
    if (p % x) == 0:
        # serialize and write to file
        nr = int(p/x)

        s = oba.serialize(format='turtle')
        filename = "OBAcat" + str(nr) + ".ttl"
        file = open(filename,"wb")
        file.write(s)
        file.close()
        oba = rdflib.Graph()
        oba.bind("dc", dc)
        oba.bind("edm", edm)
        oba.bind("foaf", foaf)

        s = nbt.serialize(format='turtle')
        filename = "NBTinOBA" + str(nr) + ".ttl"
        file = open(filename,"wb")
        file.write(s)
        file.close()
        nbt = rdflib.Graph()

if len(oba) > 0 and len(nbt) > 0:
    s = oba.serialize(format='turtle')
    filename = "OBAcat_rest.ttl"
    file = open(filename,"wb")
    file.write(s)
    file.close()

    s = nbt.serialize(format='turtle')
    filename = "NBTinOBA_rest.ttl"
    file = open(filename,"wb")
    file.write(s)
    file.close()
