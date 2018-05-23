from gensim.models import KeyedVectors
import ml_library as mll
import pandas as pd
import time
from multiprocessing import Pool
from functools import partial

def load_gensim_wordembeddings(filename):
    model = KeyedVectors.load(filename, mmap='r')
    model.syn0norm = model.syn0
    return model

wordEmbedderName = 'google.bin'
wordVectorizer = load_gensim_wordembeddings(wordEmbedderName)

def betaB(fileOmegaScores,testName,shouldRetrain=False):
    omegaScores = []
    fileList = []
    classifierName = 'beta'
    for fileName,omegaScore in fileOmegaScores.items():
        omegaScores.append(omegaScore)
        fileList.append(fileName)
    # model, isRetrained = atm.getBetaClassifier(embedVector,classifierName)
    model = mll.getKMeansClusterizer(omegaScores,classifierName,testName,shouldRetrain)
    labels = model.labels_
    df = pd.DataFrame({'fileNames':fileList,'labels':labels,'omegaScores':omegaScores})
    results = df
    return model,results

def trainUnsupervised(omegaModel, chunk):
    global wordVectorizer
    wordVectors = []
    omegaScores = []
    # f,words = chunk
    f = chunk['file_name']
    words = chunk['words_mix']
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
    return (classInput, f)

def bowToOmega(bow,testName,shouldRetrain=False):
    global wordVectorizer
    classifierName = 'omega'
    wordVecDic = {}
    for word in bow:
        try:
            # Uncomment the next line if you're using cumberbatch vectorizer
            # word = standardized_uri('en',word)
            wordVecDic[word] = wordVectorizer[word]
        except KeyError:
            pass
    # kMeansModel, clusters = atm.getOmegaClassifier(wordVecDic,classifierName)
    kMeansModel = mll.getKMeansClusterizer(wordVecDic,classifierName,testName,shouldRetrain)
    return kMeansModel

def constructBOWFromList(fileWordsList):
    BOW = []
    for item in fileWordsList:
        BOW += item['words_mix']
    BOW = list(set(BOW))
    return BOW

def trainOmega(fileWordsList,testName,shouldRetrain=False):
    bow = constructBOWFromList(fileWordsList)
    omega = bowToOmega(bow,testName,shouldRetrain)
    return omega

def trainBeta(fileList,omegaModel,testName,shouldRetrain=False):
    p = Pool(8)
    # fileList = list(fileWordsHash.items())
    func = partial(trainUnsupervised,omegaModel)
    cabrito = p.map(func,fileList)
    p.close()
    p.join()
    fileOmegaScores = {}
    for x,y in cabrito:
        if len(x) < 1:
            continue
        fileOmegaScores[y] = x

    # betaModel, fileClassDF = betaB(fileEmbed)
    return betaB(fileOmegaScores,testName,shouldRetrain)
