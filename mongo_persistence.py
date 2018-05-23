import pymongo
from pymongo import MongoClient
import ssl
import os
import numpy as np
import pandas as pd
import re

from dateutil.parser import parse
from datetime import timedelta, datetime, time
from dateutil import tz
import calendar

import math
import operator

class MongoPersistence:
    db = None
    databaseName = 'recommendations-new'    
    testName = None

    def __initDB__(self):
        client = MongoClient('mongodb://localhost:27017')
        db = client[self.databaseName]
        return db

    def resetDB(self):
        print("Going to erase the whole database.")
        self.db.file_wordsMix.delete_many({})
        self.db.recommendation_metadata.delete_many({})
        print("Database erased")

    def getWordsMixForFile(self,fileName):
        collection = self.db.file_wordsMix
        fileWordMix = list(collection.find({'file_name':fileName}))
        if len(fileWordMix) > 0:
            return fileWordMix[0]
        else:
            return None

    def setWordsMixForFile(self,fileName,wordsMix):
        collection = self.db.file_wordsMix
        collection.update({"file_name":fileName},
            {
                "$set":{"words_mix":wordsMix,"test_name":self.testName}
            },
            upsert=True
            )

    def getAllFilesWordsMix(self):
        collection = self.db.file_wordsMix
        filesWordsMix = collection.find({'test_name':self.testName})
        return list(filesWordsMix)

    def saveDF(self,df):
        collection = self.db.recommendation_metadata
        names = list(df['fileNames'])
        labels = list(df['labels'])
        omegaScores = list(df['omegaScores'])
        for idx,fileName in enumerate(names):
            tmpDic = {}
            # tmpDic['file_name'] = fileName
            tmpDic['label'] = str(labels[idx])
            tmpDic['test_name'] = self.testName
            tmpDic['omegaScore'] = omegaScores[idx]
            collection.update({'file_name':fileName},
                {
                    "$set": {
                        **tmpDic
                    }
                },
                upsert=True
                )

    def loadDocsWithLabel(self,label):
        collection = self.db.recommendation_metadata
        docs = collection.find({'label':label,'test_name':self.testName})
        return list(docs)

    def __init__(self, testName):
        self.db = self.__initDB__()
        self.testName = testName
