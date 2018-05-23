import trainning_module as trainM
import testing_module as testM
import mongo_persistence as mp
import sys

trainFolder = sys.argv[1]
testFolder = sys.argv[2]
testName = sys.argv[3]
# dbAccess = md.MemoryDatabase()
dbAccess = mp.MongoPersistence(testName)

trainM.doTrain(trainFolder,testName,dbAccess)
resultado = testM.doTests(testFolder,testName,dbAccess)
print('Resultado',resultado)
