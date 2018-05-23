class MemoryDatabase:
    filesWordsMix = {}
    bow = []
    filesCollection = {}

    def getWordsMixForFile(self,fileName):
        return self.filesWordsMix[fileName]

    def setWordsMixForFile(self,fileName,wordsMix):
        self.filesWordsMix[fileName] = wordsMix
        tmpBow = self.bow
        tmpBow += wordsMix
        self.bow = list(set(tmpBow))

    def getAllFilesWordsMix(self):
        return self.filesWordsMix

    def getBOW(self):
        return self.bow

    def saveDF(self,df):
        names = list(df['fileNames'])
        labels = list(df['labels'])
        omegaScores = list(df['omegaScores'])
        for idx,name in enumerate(names):
            tmpDic = {}
            tmpDic['fid'] = name
            tmpDic['label'] = labels[idx]
            tmpDic['omegaScore'] = omegaScores[idx]
            tmpDic['type'] = 'pdf'
            self.filesCollection[name] = tmpDic

    def getAllFilesCollection(self):
        return self.filesCollection
