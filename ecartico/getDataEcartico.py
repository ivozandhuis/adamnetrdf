#! /usr/bin/env python3

# do first (if applicable): sudo easy_install rdflib
import urllib.request
from bs4 import BeautifulSoup
import rdflib

# set vars
baseUri = "http://www.vondel.humanities.uva.nl/ecartico/"
g = rdflib.Graph()

# scrape number of last person from homepage
reply = urllib.request.urlopen(baseUri)
soup = BeautifulSoup(reply, "html.parser")
infoboxcontent = soup.find("div", attrs={'id': 'infoboxcontent'})
anchor = infoboxcontent.find('a')
href = anchor.get('href')
numberOfPersons = int(href.replace('/ecartico/persons/', ""))

# numberOfPersons = 49 # overwrite to test

# iterate and read the ecartico-person-uris
for i in range(1, numberOfPersons + 1):
    # construct uri
    uri = baseUri + "persons/" + str(i)
    print(uri) # debugging / progress

    # read graph from uri
    result = g.parse(uri) # this function *adds* the new uri to graph g

    # write every x persons into a file
    x = 1000
    if (i % x) == 0:
        # serialize and write to file
        s = g.serialize(format='turtle')
        page = int(i/x)
        filename = "ecartico" + str(page) + ".ttl"
        file = open(filename,"wb")
        file.write(s)
        file.close()
        g = rdflib.Graph()

# serialize and write to file last
if len(g) > 0:
    s = g.serialize(format='turtle')
    filename = "ecartico_rest.ttl"
    file = open(filename,"wb")
    file.write(s)
    file.close()


numberOfPlaces = 0
g = rdflib.Graph()
# iterate and read the ecartico-place-uris
for i in range(1, numberOfPlaces):
    # construct uri
    uri = baseUri + "places/" + str(i)
    print(uri) # debugging / progress

    # read graph from uri
    result = g.parse(uri) # this function *adds* the new uri to graph g
