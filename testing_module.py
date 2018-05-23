import os
import mongo_persistence as mp
import ml_library as mll
import file_text_operations as fto
import ast
from sklearn.neighbors import NearestNeighbors
from gensim.models import KeyedVectors
import sys
import time
from functools import reduce
import csv
import statistics
import numpy as np

wordEmbedderName = 'google.bin'
wordVectorizer = None
omegaModel = None
betaModel = None

# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

def load_gensim_wordembeddings(filename):
    model = KeyedVectors.load(filename, mmap='r')
    model.syn0norm = model.syn0
    return model

def getModels(testName):
    global wordVectorizer, omegaModel, betaModel
    if wordVectorizer == None:
        wordVectorizer = load_gensim_wordembeddings(wordEmbedderName)
    if omegaModel == None:
        omegaModel = mll.simpleLoadClusterizer("omega",testName)
    if betaModel == None:
        betaModel = mll.simpleLoadClusterizer("beta",testName)
    return (wordVectorizer,omegaModel,betaModel)

def recommend(dbAccess, testName, filePath, nbrOfRecommendations=1):
    wordVectorizer,omegaModel,betaModel = getModels(testName)
    try:
        words = fto.getWordsFromFile(filePath)
        wordVectors = []
        omegaScores = []
        for word in words:
            try:
                wd = wordVectorizer[word]
                wordVectors.append(wd)
            except KeyError:
                continue
        for omega in omegaModel.cluster_centers_:
            omS = mll.scoreOmega(omega,wordVectors)
            omegaScores.append(omS)
        classInput = omegaScores
        pred = betaModel.predict([classInput])
        fileLabel = pred[0]
        candidates = dbAccess.loadDocsWithLabel(str(fileLabel))
        subjects = [c['omegaScore'] for c in candidates]
        X = [classInput] + subjects

        maxRecom = len(subjects)

        if(maxRecom < 1):
            return []

        nbrs = NearestNeighbors(n_neighbors=min(nbrOfRecommendations+1,maxRecom+1), algorithm='ball_tree').fit(X)
        distances, indices = nbrs.kneighbors(X)
        selected = []
        indexeses = list(indices[0,1:])
        distanxeses = list(distances[0,1:])
        # print("distanxeses",distanxeses)
        for indice in indexeses:
            selected.append(candidates[indice-1])

        tmp = filePath.split(os.path.sep)
        fid = tmp[len(tmp)-1]
        return {
                "fid": fid,
                "recommendations": [
                    {
                        "fid": s['file_name'],
                        "distance": distanxeses[i]
                    }
                    for i,s in enumerate(selected)
                ],
                "min":distanxeses[0],
                "max":distanxeses[len(distanxeses)-1],
                "median":statistics.median(distanxeses),
                "std":np.std(distanxeses),
                "avg_distance": reduce(lambda x, y: x + y, distanxeses) / len(distanxeses),
                "nbr_words":len(list(set(words)))
            }


    except ValueError as e:
        print("Value Error",str(e))

def scoreOneResult(recommendation):
    fileClass = recommendation['fid'].split('.')[0]
    recom = recommendation['recommendations'][0]
    recomClass = recom['fid'].split('.')[0]
    if fileClass == recomClass:
        return 1
    else:
        return 0

def scoreAtLeastOneResult(recommendation):
    fileClass = recommendation['fid'].split('.')[0]
    recom = recommendation['recommendations']
    for item in recom:
        recomClass = item['fid'].split('.')[0]
        if fileClass ==  recomClass:
            return 1
    return 0

def scoreDistResult(recommendation):
    score = 0
    fileClass = recommendation['fid'].split('.')[0]
    recom = recommendation['recommendations']
    divisible = len(recom)
    for item in recom:
        recomClass = item['fid'].split('.')[0]
        if fileClass ==  recomClass:
            score += 1

    return score / divisible


def doTests(folderPath, testName, dbAccess,kNumber=5):
    fileList = os.listdir(folderPath)
    getModels(testName)
    oneScore = 0
    atLeastOneScore = 0
    totalScore = 0
    # kNumber = 2
    print("KNUMBER",2)

    start_time = time.time()
    print("Initializing the Test Phase.")

    l = len(fileList)
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

    results = {}
    for k in range(1,kNumber+1):
        results[k] = {'totalScore':0, 'atLeastOneScore':0, 'avg_distance':[]}

    for i, filePath in enumerate(fileList):
        for k in range(1,kNumber+1):
            try:
                # recommendations = recommend(dbAccess, testName, os.path.join(folderPath,filePath), k)
                # oneScore += scoreOneResult(recommendations)
                # atLeastOneScore += scoreAtLeastOneResult(recommendations)
                # totalScore += scoreDistResult(recommendations)

                recommendationResults = recommend(dbAccess, testName, os.path.join(folderPath,filePath), k)
                results[k]['atLeastOneScore'] += scoreAtLeastOneResult(recommendationResults)
                results[k]['totalScore'] += scoreDistResult(recommendationResults)
                results[k]['avg_distance'].append(recommendationResults['avg_distance'])
                printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
            except TypeError:
                print("Could not recommend for",filePath)
                print("recommendations",recommendationResults)

    # oneAccuracy = (oneScore / len(fileList)) * 100
    # atLeastOneAccuracy = (atLeastOneScore / len(fileList)) * 100
    # totalAccuracy = (totalScore / len(fileList)) * 100
    for k in range(1,kNumber+1):
        results[k]['atLeastOneScore'] = (results[k]['atLeastOneScore'] / len(fileList)) * 100
        results[k]['totalScore'] = (results[k]['totalScore'] / len(fileList)) * 100
        results[k]['avg_distance'] = reduce(lambda x, y: x + y, results[k]['avg_distance']) / len(results[k]['avg_distance'])

        print("K=",k)
        print("At least one doc recommendation:",results[k]['atLeastOneScore'],"%")
        print("The total accuracy was",results[k]['totalScore'],"%")
        print("Average distance is",results[k]['avg_distance'])
    print("Testing finished in %.2f seconds." % (time.time() - start_time))


    # print("Closest one recommendation:",oneAccuracy,"%")
    # print("At least one doc recommendation:",atLeastOneAccuracy,"%")
    # print("The total accuracy was",totalAccuracy,"%")
    # print("Testing finished in %.2f seconds." % (time.time() - start_time))

    return results
    # return {
        # 'oneAccuracy':oneAccuracy,
        # 'atLeastOneScore':atLeastOneAccuracy,
        # 'totalAccuracy':totalAccuracy,
        # 'testingTime': (time.time() - start_time)
    # }

def getMinK(recommendationObject):
    fileClass = recommendationObject['fid'].split('.')[0]
    recommendations = recommendationObject['recommendations']
    k = 1
    baseDistance = recommendations[0]['distance']
    for item in recommendations:
        recomClass = item['fid'].split('.')[0]
        if fileClass ==  recomClass:
            distanceToBase = item['distance'] - baseDistance
            distanceToOrigin = item['distance']
            # ratio = distanceToBase / distanceToOrigin
            ratio = item['distance'] / baseDistance
            return (k, distanceToBase, distanceToOrigin, ratio)
        k+=1
    return (-100, -100, -100, -100)

def kDistanceTest(folderPath, testName, dbAccess, csvFileName):
    fileList = os.listdir(folderPath)
    getModels(testName)

    start_time = time.time()
    print("K Distance Test Started.")

    l = len(fileList)
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

    results = []

    for i, filePath in enumerate(fileList):
        try:
            tmpDic = {}
            recommendationResults = recommend(dbAccess, testName, os.path.join(folderPath,filePath), 100)
            # print("recommendationResults",recommendationResults)
            minK, distanceFirstPred, distanceToOrigin, distanceRatio = getMinK(recommendationResults)
            tmpDic['dataset'] = testName
            fileClass = recommendationResults['fid'].split('.')[0]
            tmpDic['id'] = recommendationResults['fid']
            tmpDic['minK'] = minK
            tmpDic['nbr_words'] = recommendationResults['nbr_words']
            tmpDic['class'] = fileClass
            tmpDic['distanceFirstPred'] = distanceFirstPred
            tmpDic['distanceToOrigin'] = distanceToOrigin
            tmpDic['distanceRatio'] = distanceRatio

            tmpDic["min"] = recommendationResults['min']
            tmpDic["max"] = recommendationResults['max']
            tmpDic["median"] = recommendationResults['median']
            tmpDic["std"] = recommendationResults['std']
            results.append(tmpDic)
            printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        except TypeError:
            print("Could not recommend for",filePath)
            print("recommendations",recommendationResults)

    fieldnames = ['dataset','nbr_words','id','minK','class', 'distanceFirstPred', 'distanceToOrigin', 'distanceRatio']
    fieldnames += ['min', 'max', 'median', 'std']
    # fieldnames = list(resultsDict[list(resultsDict.keys())[0]][1].keys())

    file_exists = os.path.isfile(csvFileName)
    with open(csvFileName, 'a+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
        for item in results:
            writer.writerow({**item})

    print("K Distance Test finished in %.2f seconds." % (time.time() - start_time))

    return results

if __name__ == "__main__":
    testFolder = sys.argv[1]
    testName = sys.argv[2]
    dbAccess = mp.MongoPersistence(testName)
    doTests(testFolder,testName,dbAccess)
