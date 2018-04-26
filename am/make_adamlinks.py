#! /usr/bin/env python3

import rdflib
import os

# set namespaces
owl  = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
rdf  = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
edm  = rdflib.Namespace("http://www.europeana.eu/schemas/edm/")
void = rdflib.Namespace("http://rdfs.org/ns/void#")

dataset = rdflib.URIRef("https://data.adamlink.nl/am/amcollect/")

# read AdamLinkGraphs into dict
owl = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
g = rdflib.Graph()

result = g.parse("adamlinkpersonen.ttl", format="turtle")
print("AdamLink Person URI's are read")
result = g.parse("adamlinkstraten.ttl", format="turtle")
print("AdamLink Street URI's are read")
result = g.parse("adamlinkgebouwen.ttl", format="turtle")
print("AdamLink Building URI's are read")

adamLinkUris = {}
for s,_,o in g.triples((None, owl.sameAs, None)):
    adamLinkUris[o] = s

adamLinkUriSet = set(adamLinkUris.keys())

# process original ttl-files
ttlFiles = [x for x in os.listdir() if x.endswith(".org.ttl")]
for infile in ttlFiles:
    print(infile) # print progress

    # read file into graph-object
    g = rdflib.Graph()
    g.namespace_manager.bind('void', void, override=False)
    result = g.parse(infile, format="turtle")

    # do AdamLink changes
    for s,p,o in g.triples((None, None, None)):

        # replace person uri's
        if o in adamLinkUriSet:
            g.remove((s,p,o))
            g.add((s,p,adamLinkUris[o]))

        # add void:inDataset
        if p == rdf.type and o == edm.providedCHO:
            g.add((s,void.inDataset, dataset))

    # write new turtle-file
    outfile = infile
    outfile = outfile.replace(".org.",".adm.")
    s = g.serialize(format='turtle')
    f = open(outfile,"wb")
    f.write(s)
    f.close()
