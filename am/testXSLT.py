#! /usr/bin/env python3

import lxml.etree as etree
from urllib.parse import urlencode
import rdflib

# initiate XSLT
xslt = etree.parse("adlibXML2rdf.xslt")
transform = etree.XSLT(xslt)

# initialize variables for loop
page = 0
numberFound = 1000000
numberShow = 100

# iterate through resultpages
while (numberFound > (page * numberShow)):
    start = page * numberShow

    # read page of records
    requestUrl = "http://amdata.adlibsoft.com/wwwopac.ashx?database=AMcollect&search=all&limit=" + str(numberShow) + "&startfrom=" + str(start)
    print(requestUrl)
    dom = etree.parse(requestUrl)

    # read numberFound
    hits = dom.find(".//hits")
    numberFound = int(hits.text)
#    numberFound = 500 # by overwriting you can shortcut for testing

    # transform into RDF/XML
    newdom = transform(dom)
    rdfxml = etree.tostring(newdom, pretty_print=True)

    # write rdfxml-file
#    filename = "am" + str(page) + ".rdf.xml"
#    f = open(filename,"wb")
#    f.write(rdfxml)
#    f.close()

    # read into rdf-graph object and serialize as turtle
    g = rdflib.Graph()
    r = g.parse(data=rdfxml, format="xml")
    s = g.serialize(format='turtle')

    # write turtle-file
    filename = "am" + str(page) + ".org.ttl"
    f = open(filename,"wb")
    f.write(s)
    f.close()

    page = page + 1
