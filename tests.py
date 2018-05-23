import csv
csvFileName = 'results.csv'
resultsDict = {}


resultsDict['r8'] = {1:{'totalScore':1, 'atLeastOneScore':1, 'avg_distance':1},2:{'totalScore':2, 'atLeastOneScore':2, 'avg_distance':2}}
resultsDict['r7'] = {1:{'totalScore':8, 'atLeastOneScore':8, 'avg_distance':8},2:{'totalScore':9, 'atLeastOneScore':10, 'avg_distance':11}}

fieldnames = ['expName','k'] + list(resultsDict[list(resultsDict.keys())[0]][1].keys())
with open(csvFileName, 'w+', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for expName, expDict in resultsDict.items():
        print("expName",expName)
        print("EXPDICT",expDict)
        for k,value in expDict.items():
            print("VALUE",*value)
            writer.writerow({'expName':expName, 'k':k, **value})
