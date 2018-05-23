import trainning_module as trainM
import testing_module as testM
import mongo_persistence as mp
import sys
import os
import json
import csv

fileName = "order.txt"
datasetFolder = "datasets"

# csvFileName = 'results.csv'
resultsDict = {}

def writeAccuracyTestResults(csvFileName, resultsDictionary):
    fieldnames = ['expName','k'] + list(resultsDict[list(resultsDict.keys())[0]][1].keys())
    with open(csvFileName, 'w+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for expName, expDict in resultsDict.items():
            for k,value in expDict.items():
                writer.writerow({'expName':expName, 'k':k, **value})

def writeTXTResults(testName,results):
    with open('results/results-'+testName+'.txt','w') as f2:
        f2.write(json.dumps(resultado))
        f2.close()

with open(fileName) as f:
    for line in f:
        testName = line.rstrip()
        trainFolder = os.path.join(datasetFolder,testName,'train')
        testFolder = os.path.join(datasetFolder,testName,'test')
        print("TRAIN_FOLDER",trainFolder)
        print("TEST_FOLDER",testFolder)
        print("Test Name",testName)

        dbAccess = mp.MongoPersistence(testName)
        # trainM.doTrain(trainFolder,testName,dbAccess)

        csvFileName = 'kDistanceTest.csv'
        kDistResults = testM.kDistanceTest(testFolder,testName,dbAccess, csvFileName)

        # resultsDict[testName] = resultado
        # kNumber = 7
        # resultado = testM.doTests(testFolder,testName,dbAccess,kNumber)
        # writeTXTResults(testName,resultado)
        # resultsDict[testName] = resultado

# writeAccuracyTestResults('results.csv',resultsDict)
