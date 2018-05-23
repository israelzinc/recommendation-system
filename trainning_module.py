import file_text_operations as fto
import models_trainner as mt
import memory_database as md
import mongo_persistence as mp
import time
import sys
import os

def doTrain(trainFolder,testName,dbAccess):
    print("Starting the train Phase")
    start_time = time.time()
    BOW = fto.constructBOWFromFolder(trainFolder,dbAccess)
    fileWordsList = dbAccess.getAllFilesWordsMix()
    omegaModel = mt.trainOmega(fileWordsList,testName)
    betaModel,fileClassDF = mt.trainBeta(fileWordsList,omegaModel,testName)
    dbAccess.saveDF(fileClassDF)
    print("Trainning finished in %.2f seconds." % (time.time() - start_time))

if __name__ == "__main__":
    trainFolder = sys.argv[1]
    testName = sys.argv[2]
    dbAccess = mp.MongoPersistence(testName)
    doTrain(trainFolder,testName,dbAccess)
