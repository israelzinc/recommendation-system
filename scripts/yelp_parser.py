import json

# fileName = "yelp_sample.txt"
fileName = "review.json"

reviews = []
train_counters = {}
test_counters = {}
min_stars = 0
max_stars = 5
maximum_nbr_files = 1000
targetFolder = "./separated/"
trainFolder = targetFolder+"/train/"
testFolder = targetFolder+"/test/"
for x in range(min_stars,max_stars+1):
    train_counters[x] = 0
    test_counters[x] = 0

def checkTermination(counterDictionary,maximum_nbr_files,max_stars):
    expectedTotal = maximum_nbr_files * max_stars
    total = 0
    for val in counterDictionary.values():
        total += val
    if expectedTotal == total:
        return True
    else:
        return False


with open(fileName) as f:
    for line in f:
        rev = json.loads(line)
        stars = int(rev['stars'])
        if train_counters[stars] < maximum_nbr_files:
            fileName = trainFolder + str(stars) + '.'+str(train_counters[stars])+'.txt'
            train_counters[stars] += 1
            f2 = open(fileName, 'w')
            f2.write(rev['text'])
            f2.close()
        elif test_counters[stars] < maximum_nbr_files:
            fileName = testFolder + str(stars) + '.'+str(test_counters[stars])+'.txt'
            test_counters[stars] += 1
            f2 = open(fileName, 'w')
            f2.write(rev['text'])
            f2.close()
        else:
            t1 = checkTermination(train_counters,maximum_nbr_files,max_stars)
            t2 = checkTermination(test_counters,maximum_nbr_files,max_stars)
            if t1 == True and t2 == True:
                print("Gonna terminate")
                break;
