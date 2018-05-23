import os
import pandas as pd
import numpy as np
import pickle
from sklearn.cluster import KMeans
import time
from scipy.spatial import distance
import math

classFunctions = {}
classFunctions['omega'] = 'omegarizeBOW'
classFunctions['beta'] = 'trainBeta'
modelsFolder = "models"

#TODO: treat error in case its not avaliable
def simpleLoadClusterizer(name,version):
	className = getClusterizerName(name,version)
	with open(className+".pkl",'rb') as fid:
		return pickle.load(fid)

def getClusterizerName(name,version):
	return os.path.join(modelsFolder,name+"-"+version)

def getKMeansClusterizer(X, classifierName, version, re_train=False):
	try:
		className = getClusterizerName(classifierName,version)
		funcName = classFunctions[classifierName]
		func = eval(funcName)
		if(os.path.isfile(className+".pkl")):
			if(re_train == False):
				try:
					with open(className+".pkl",'rb') as fid:
						return pickle.load(fid)
				except EOFError:
					classifier = func(X)
					with open(className+".pkl",'wb') as fid:
						pickle.dump(classifier,fid)
					return classifier

		# If the classifier does not exist or you have to train it again
		classifier = func(X)
		with open(className+".pkl",'wb') as fid:
		    pickle.dump(classifier,fid)
		return classifier

	except KeyError as e:
		print("Error while trying to create a function for ",classifierName)

def omegarizeBOW(bow):

	maxScore = 10000000
	maxModel = None
	maxNbrCluster = None

	we = pd.DataFrame.from_dict(bow, orient='index')
	we.index.rename('uri', True)

	print("TextML: Could assign {} word vectors".format(we.shape[0]))
	we = we.dropna()

	print("TextML: Initiating the Omega trainning phase")
	start_time = time.time()
	mat = we.as_matrix(range(300))

	scale = 0.1

	# Modificaton to make it run faster (Only for testing purposes)
	l_bound = 4
	u_bound = 16

	print("Optimizing Omega")
	for num_clusters in range(l_bound,u_bound):
	    cluster = KMeans(n_clusters=num_clusters, max_iter=100, n_jobs=1)
		# MacOS needs to run in exactly 1 job otherwise it never stop running
	    # cluster = KMeans(n_clusters=num_clusters, max_iter=300, n_jobs=-1)
	    cluster.fit(mat)
	    rc = cluster.score(mat)
	    score = -rc / mat.shape[0]
	    # print("Score for",num_clusters,"is",score)
	    maxModel = cluster
	    if(score < maxScore):
	        maxModel = cluster
	        maxScore = score
	        maxNbrCluster =num_clusters

	print("Omega with Max Score is",maxNbrCluster)
	print("The maxScore is",maxScore)
	labels = maxModel.labels_
	print("TextML: Omega train finished in %.2f seconds." % (time.time() - start_time))
	return maxModel
    # results = pd.DataFrame([we.index,labels]).T
	# return (maxModel,results)
	# return maxModel

def trainBeta(X):
    l_bound = 4
    u_bound = 16

    maxScore = 10000000
    maxModel = None
    maxNbrCluster = None

    scale = 0.1

    start_time = time.time()

    for num_clusters in range(l_bound,u_bound):
        cluster = KMeans(n_clusters=num_clusters, max_iter=100, n_jobs=-1)
        cluster.fit(X)
        rc = cluster.score(X)
        score = -rc / len(X)
        # print("Score for",num_clusters,"is",score)
        maxModel = cluster
        if(score < maxScore):
            maxModel = cluster
            maxScore = score
            maxNbrCluster =num_clusters

    print("Beta with Max Score is",maxNbrCluster)
    print("The maxScore is",maxScore)
    print("TextML: Beta train finished in %.2f seconds." % (time.time() - start_time))
    return maxModel

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def scoreOmega(omegaCentroid,distancesMatrix):
	# print("DISTANCE MATRIX",distancesMatrix)
	score = 0
	testDiv = len(distancesMatrix)
	if testDiv == 0:
		testDiv = 1
	for word in distancesMatrix:
		d = distance.euclidean(omegaCentroid,word)
		score += sigmoid(d)
	return score/testDiv
	# return score/len(distancesMatrix)
