#!/usr/bin/env python3
import sys
import spacy

if len(sys.argv) != 3:
    print("Usage: tag.py <inputfile> <outputfile>")
    sys.exit(-1)

input = open(sys.argv[1], "r").read()
output = open(sys.argv[2], "w")

nlp = spacy.load("en_core_web_lg")
doc = nlp(input)

for token in doc:
    output.write("{text} {lemma} {pos} {tag} {dep} {shape} {is_alpha} {is_stop}\n".format(
        text=token.text, lemma=token.lemma_, pos=token.pos_, tag=token.tag_, dep=token.dep_,
        shape=token.shape_, is_alpha=token.is_alpha, is_stop=token.is_stop
    ))
