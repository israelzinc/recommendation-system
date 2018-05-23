from subprocess import PIPE, run
from urllib.parse import urlparse
import string
import re
import os

def getWordsMix(pg):
    pg_words = []
    numberOfWords = 0

    for lexem in pg.split():

        # print("LEXEM",lexem)
        # if len(lexem) < 4:
        #     continue

        numberOfWords += 1

        if urlparse(lexem).scheme in [ 'https', 'http' ]:
            continue
        elif re.match("^[0-9]+$", lexem):
            continue
        else:
            lexem_without_punctuation = lexem.translate(str.maketrans('','',string.punctuation))
            for ll in lexem_without_punctuation.split():
                # if len(ll) < 4:
                #     continue
                pg_words.append(ll)

    # tooCommonWords = stopwords.words('english') + ['this', 'which', 'that', 'return']
    # wordMix = [tok.lower() for tok in pg_words if len(tok.lower()) > 1 and (tok.lower() not in tooCommonWords)]
    wordMix = [tok.lower() for tok in pg_words if len(tok.lower()) > 1]
    uniqueWords = list(set(wordMix))
    return uniqueWords

def getAllWords(pg):
    pg_words = []
    numberOfWords = 0

    for lexem in pg.split():

        # print("LEXEM",lexem)
        # if len(lexem) < 4:
        #     continue

        numberOfWords += 1

        if urlparse(lexem).scheme in [ 'https', 'http' ]:
            continue
        elif re.match("^[0-9]+$", lexem):
            continue
        else:
            lexem_without_punctuation = lexem.translate(str.maketrans('','',string.punctuation))
            for ll in lexem_without_punctuation.split():
                # if len(ll) < 4:
                #     continue
                pg_words.append(ll)

    # tooCommonWords = stopwords.words('english') + ['this', 'which', 'that', 'return']
    # wordMix = [tok.lower() for tok in pg_words if len(tok.lower()) > 1 and (tok.lower() not in tooCommonWords)]
    # wordMix = [tok.lower() for tok in pg_words if len(tok.lower()) > 1]
    # uniqueWords = list(set(wordMix))
    return pg_words

def getAllWordsFromFile(filePath):
    # textCmdResult = run([ 'pdftotext', filePath, '-' ], stdout=PIPE, universal_newlines=True)
    fileObj = open(filePath, 'r')
    words = getAllWords(fileObj.read())
    return words

# This returns only the wordMix
def getWordsFromFile(filePath):
    # textCmdResult = run([ 'pdftotext', filePath, '-' ], stdout=PIPE, universal_newlines=True)
    fileObj = open(filePath, 'r')
    words = getWordsMix(fileObj.read())
    return words

def constructBOWFromFolder(folderPath,dbAccess):
    BOW = []
    fileList = os.listdir(folderPath)
    for f in fileList:
        try:
            words = getWordsFromFile(os.path.join(folderPath,f))
        except UnicodeDecodeError:
            print("Training: Got unicode error, skipping doc",f)
            continue
        dbAccess.setWordsMixForFile(f,words)
        BOW += words
    BOW = list(set(BOW))
    return BOW
