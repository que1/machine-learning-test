__author__ = 'admin'

import numpy as np

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec

def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word: %s is not in my Vocabulary!" % word)
    return returnVec

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    #p0Num = np.zeros(numWords); p1Num = np.zeros(numWords)
    p0Num = np.ones(numWords); p1Num = np.ones(numWords)      #change to ones()
    #p0Denom = 0.0; p1Denom = 0.0
    p0Denom = 2.0; p1Denom = 2.0                        #change to 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
            print("1-", i, p1Num, p1Denom)
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
            print("0-", i, p0Num, p0Denom)
    #p1Vect = p1Num/p1Denom
    #p0Vect = p0Num/p0Denom
    p1Vect = np.log(p1Num/p1Denom)  #change to log()
    p0Vect = np.log(p0Num/p0Denom)       #change to log()
    return p0Vect, p1Vect, pAbusive

if __name__ == '__main__':
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))

    p0Vect, p1Vect, pAbusive = trainNB0(trainMat, listClasses)
    print(p0Vect, p1Vect, pAbusive)
