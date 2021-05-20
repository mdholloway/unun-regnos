#!/usr/bin/env python3
import sys
import spacy
import sklearn
import numpy as np


def clusterTokens(needsClustering):
    #takes a set of tokens and returns a list of lists, one sublist per cluster
    clusters = []
    tokenArray = np.array()
    vectorToTokenMap = {}

    NUM_CLUSTERS = len(needsClustering) // 2.4
    for token in needsClustering:
            if (token.vector()):
                vectorToTokenMap[token.vector()] = token
                tokenArray.add(token.vector())
            else:
                clusters += [token]

    clusterer = sklearn.KMeans(n_clusters=NUM_CLUSTERS)
    clusterer.fit(tokenArray)
    clusterArray = clusterer.predict(tokenArray)
    #for degugging/entertainment purposes
    print(clusterArray)
    #mapp vector back to tokens and create clusters
    for (cluster_index,vector) in clusterArray:
        if clusters[cluster_index]:
            clusters[cluster_index].add(vectorToTokenMap[vector])
        else:
            clusters[cluster_index] = [vectorToTokenMap[vector]]
    return clusters

if len(sys.argv) != 3:
    print("Usage: spacy.py <inputfile> <outputfile>")
    sys.exit(-1)

input = open(sys.argv[1], "r").read()
output = open(sys.argv[2], "w")

nlp = spacy.load("en_core_web_lg")
doc = nlp(input)

lemmaToTranslationMap = {}
needsClustering = set([])

for token in doc:
    #untranslated classes;__FUTURE__ handle NUMERAL and PROPN seperately?
    if token.pos_ in ["PUNCT","SYM","X","NUMERAL","PROPN"]: lemmaToTranslationMap[token.lemma_] = token.text
    #eligible for semanitic clustering
    elif token.pos_ in ["NOUN"]: nounsForClustering.add(token)
    elif token.pos_ in ["VERB","ADV","ADJ","INTJ"]: verbalsForClustering.add(token)
    #Closed classes, some of these are not classes in Unun Regnos but for now we generate them all
    elif token.pos_ in ["DET", "AUX", "ADP", "SCONJ", "CCONJ"]: lemmaToTranslationMap[token.lemma_] = generateFunctionWord()

clustersToTranslate = clusterTokens(nounsForClustering)
clustersToTranslate.extend(clusterTokens(verbalsForClustering))
lemmaToTranslationMap = {}

for thisCluster in clustersToTranslate:
    cluster_root = generateRoot()
    for token in thisCluster:
        if token.lemma_ not in lemmaToTranslationMap:
            translation = cluster_root
            while (translation == cluster_root): translation = expandRoot(cluster_root)
            lemmaToTranslationMap[token.lemma_] = translation

for token in doc:
    output.write("{text} {lemma} {translation}\n".format(text=token.text, lemma=token.lemma_, translation=lemmaToTranslationMap[token.lemma_]))
output.write(lemmaToTranslationMap)
