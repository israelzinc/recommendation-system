import file_text_operations as fto
import time
from functools import reduce
import sys
import os
import common_functions as comF
import json
import csv
import numpy as np

def getStatisticsForDataset(folderPath):
    start_time = time.time()

    wordFiles = {}
    docUniqueWordsCount = {}
    docWordsCount = {}
    docDiffWordsCount = {}

    fileList = os.listdir(folderPath)
    nbrDocs = 0
    nbrDocsUniqueWords = 0
    nbrUniqueWords = 0

    bow = []

    avgUniqueWordsDoc = []
    avgWordsDoc = []
    avgDiffWordsDoc = []
    avgLenWords = []
    l = len(fileList)

    classStats = {}
    for i, f in enumerate(fileList):
        try:
            fileClass = f.split('.')[0]

            words = fto.getAllWordsFromFile(os.path.join(folderPath,f))
            wordMix = [tok.lower() for tok in words if len(tok.lower()) > 1]
            diffWordsList = list(set(wordMix))
            for w in diffWordsList:
                if not w in wordFiles:
                    wordFiles[w] = []
                wordFiles[w].append(f)
            docWordsCount[f] = len(words)
            docDiffWordsCount[f] = diffWordsList
            docUniqueWordsCount[f] = 0
            nbrDocs += 1
            bow += words
            avgWordsDoc.append(len(words))
            avgDiffWordsDoc.append(len(diffWordsList))

            if fileClass not in classStats:
                classStats[fileClass] = {}

            if 'words' not in classStats[fileClass]:
                classStats[fileClass]['words'] = []
            classStats[fileClass]['words'] += diffWordsList

            if 'nbrDocs' not in classStats[fileClass]:
                classStats[fileClass]['nbrDocs'] = 0
            classStats[fileClass]['nbrDocs'] += 1

            comF.printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        except UnicodeDecodeError:
            print("Training: Got unicode error, skipping doc",f)
            continue

    for k,v in wordFiles.items():
        if len(v) < 2:
            fileClass = v[0].split('.')[0]
            if 'uniqueWords' not in classStats[fileClass]:
                classStats[fileClass]['uniqueWords'] = []
            classStats[fileClass]['uniqueWords'].append(k)
            # print(k,"eh uma palavra unica do documento",v[0])
            docUniqueWordsCount[v[0]] += 1
            # print("SERA?",k,wordFiles[k])

    for k,v in docUniqueWordsCount.items():
        if(v > 0):
            # print("Document",k,"has",v,"unique words.")
            avgUniqueWordsDoc.append(v)
            nbrUniqueWords += v
            nbrDocsUniqueWords += 1

    print(len(avgUniqueWordsDoc))
    c_avgUniqueWordsDoc = reduce(lambda x, y: x + y, avgUniqueWordsDoc) / nbrDocs

    for w in bow:
        avgLenWords.append(len(w))

    avgDiffWordsDoc = reduce(lambda x, y: x + y, avgDiffWordsDoc) / len(avgDiffWordsDoc)
    avgUniqueWordsDoc = reduce(lambda x, y: x + y, avgUniqueWordsDoc) / len(avgUniqueWordsDoc)
    avgWordsDoc = reduce(lambda x, y: x + y, avgWordsDoc) / len(avgWordsDoc)
    avgLenWords = reduce(lambda x, y: x + y, avgLenWords) / len(avgLenWords)

    bowSize = len(list(set(bow)))
    results = {}
    results['nbrDocs'] = nbrDocs
    results['bowSize'] = bowSize
    results['nbrUniqueWords'] = nbrUniqueWords
    results['nbrDocsUniqueWords'] = nbrDocsUniqueWords
    results['avgLenWords'] = avgLenWords
    results['avgWordsDoc'] = avgWordsDoc
    results['avgDiffWordsDoc'] = avgDiffWordsDoc
    results['c_avgUniqueWordsDoc'] = c_avgUniqueWordsDoc
    results['ratio_wordsDocByuniqWordsDoc'] = avgWordsDoc/c_avgUniqueWordsDoc
    results['ratio_wordsDocBYdiffWordsDoc'] = avgWordsDoc/avgDiffWordsDoc
    results['ratio_bowSizeBYnbrUniqueWords'] = bowSize/nbrUniqueWords
    results['ratio_bowSizeBYnbrDocs'] = bowSize/nbrDocs

    # print("DSDSADSAD",fileClass)

    avgUniqueWordsClass = []
    avgDiffWordsClass = []
    avgDocsClass = []
    for className,classDictionary in classStats.items():


        uw = classDictionary['uniqueWords']
        uw = list(set(uw))
        avgUniqueWordsClass.append(len(uw))
        # classDictionary['uniqueWords'] = uw
        lenWords = len(list(set(classDictionary['words'])))
        avgDiffWordsClass.append(lenWords)
        avgDocsClass.append(classDictionary['nbrDocs'])
        # classDictionary['nbrWords'] = lenWords
        # classDictionary['nbrUniqueWords'] = len(uw)
        # classDictionary['avgUniqueWords'] = len(uw) / classDictionary['nbrDocs']

    resultsClassDict = {}
    # resultsClassDict['avgUniqueWordsDoc'] = reduce(lambda x, y: x + y, avgUniqueWordsClass) / len(avgUniqueWordsClass)
    # resultsClassDict['avgDiffWordsClass'] = reduce(lambda x, y: x + y, avgDiffWordsClass) / len(avgDiffWordsClass)
    # resultsClassDict['avgDocsClass'] = reduce(lambda x, y: x + y, avgDocsClass) / len(avgDocsClass)
    #
    # resultsClassDict['stdUniqueWordsDoc'] = sum([(xi - resultsClassDict['avgUniqueWordsDoc']) ** 2 for xi in avgUniqueWordsClass]) / (len(avgUniqueWordsClass) - 1)
    # resultsClassDict['stdDiffWordsClass'] = sum([(xi - resultsClassDict['avgDiffWordsClass']) ** 2 for xi in avgDiffWordsClass]) / (len(avgDiffWordsClass) - 1)
    # resultsClassDict['stdDocsClass'] = sum([(xi - resultsClassDict['avgDocsClass']) ** 2 for xi in avgDocsClass]) / (len(avgDocsClass) - 1)

    # results['class_avgUniqueWordsDoc'] = reduce(lambda x, y: x + y, avgUniqueWordsClass) / len(avgUniqueWordsClass)
    # results['class_avgDiffWordsClass'] = reduce(lambda x, y: x + y, avgDiffWordsClass) / len(avgDiffWordsClass)
    # results['class_avgDocsClass'] = reduce(lambda x, y: x + y, avgDocsClass) / len(avgDocsClass)
    #
    # results['class_stdUniqueWordsDoc'] = sum([(xi - results['class_avgUniqueWordsDoc']) ** 2 for xi in avgUniqueWordsClass]) / (len(avgUniqueWordsClass) - 1)
    # results['class_stdDiffWordsClass'] = sum([(xi - results['class_avgDiffWordsClass']) ** 2 for xi in avgDiffWordsClass]) / (len(avgDiffWordsClass) - 1)
    # results['class_stdDocsClass'] = sum([(xi - results['class_avgDocsClass']) ** 2 for xi in avgDocsClass]) / (len(avgDocsClass) - 1)

    meanUniqueWordsClass = np.mean(avgUniqueWordsClass)
    meanDiffWordsClass = np.mean(avgDiffWordsClass)
    meanDocsClass = np.mean(avgDocsClass)

    stdUniqueWordsClass = np.std(avgUniqueWordsClass)
    stdDiffWordsClass = np.std(avgDiffWordsClass)
    stdDocsClass = np.std(avgDocsClass)

    print("UNIQUEWORDSCLASS",avgUniqueWordsClass)
    print("DIFFWORDSCLASS",avgDiffWordsClass)
    print("DOCSCLASS",avgDocsClass)

    results['class_avgUniqueWordsClass'] = meanUniqueWordsClass
    results['class_avgDiffWordsClass'] = meanDiffWordsClass
    results['class_avgDocsClass'] = meanDocsClass
    results['class_stdUniqueWordsClass'] = stdUniqueWordsClass
    results['class_stdDiffWordsClass'] = stdDiffWordsClass
    results['class_stdDocsClass'] = stdDocsClass


    # print("Number of Documents:",nbrDocs)
    # print("BOW Size:",bowSize)
    # print("Number of Unique Words",nbrUniqueWords)
    # print("Number of Docs with Unique Words",nbrDocsUniqueWords)
    # print("AVG len of words in BOW:",avgLenWords)
    # print("AVG DOC SIZE:",avgWordsDoc)
    # print("AVG DIFF WORDS DOC:",avgDiffWordsDoc)
    # print("AVG UNQ WORDS DOC:",c_avgUniqueWordsDoc)
    print("Statistics done in %.2f seconds." % (time.time() - start_time))
    return results

if __name__ == "__main__":
    fileName = "order.txt"
    datasetFolder = "datasets"
    csvFileName = 'docs_statistics.csv'
    csvClassFileName = 'class_statistics.csv'
    resultsDict = {}
    with open(fileName) as f:
        for line in f:
            testName = line.rstrip()
            trainFolder = os.path.join(datasetFolder,testName,'train')
            resultado = getStatisticsForDataset(trainFolder)
            print("Test Name",testName)
            with open('statistics/results-'+testName+'.txt','w') as f2:
                f2.write(json.dumps(resultado))
                f2.close()
            resultsDict[testName] = resultado

    fieldnames = ['expName'] + list(resultsDict[list(resultsDict.keys())[0]])
    with open(csvFileName, 'w+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for expName, value in resultsDict.items():
            writer.writerow({'expName':expName, **value})
