#! /usr/bin/env python3

import lxml.etree as etree
import rdflib

# initialize variables for loop
page = 0
numberFound = 1000000
numberShow = 100

# read numberFound
requestUrl = "http://amdata.adlibsoft.com/wwwopac.ashx?database=AMcollect&search=all"
print(requestUrl)
dom = etree.parse(requestUrl)
hits = dom.find(".//hits")
numberFound = int(hits.text)
numberFound = 101 # by overwriting you can shortcut for testing

# iterate through resultpages
while (numberFound > (page * numberShow)):
    start = page * numberShow

    # read page of records
    requestUrl = "http://amdata.adlibsoft.com/wwwopac.ashx?database=lod-AMobjects&search=all&limit=" + str(numberShow) + "&startfrom=" + str(start)
    print(requestUrl)
    dom = etree.parse(requestUrl)

    # create rdfxml-string
    rdfxml = etree.tostring(dom, pretty_print=True)

    # read into rdf-graph object and serialize as turtle
    g = rdflib.Graph()
    r = g.parse(data=rdfxml, format="xml")
    s = g.serialize(format='turtle')

    # write turtle-file
    filename = "am" + str(page) + ".ttl"
    f = open(filename,"wb")
    f.write(s)
    f.close()

    page = page + 1
