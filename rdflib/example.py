#! /usr/bin/env python3

# do first (if applicable): sudo easy_install rdflib
import rdflib

g = rdflib.Graph()
# general example
result = g.parse("https://www.zuiderzeecollectie.nl/object/collect/34576")

print("graph has %s statements." % len(g))

for subj, pred, obj in g:
   if (subj, pred, obj) not in g:
       raise Exception("It better be!")

s = g.serialize(format='n3')

print(s)
