from gensim.models import KeyedVectors
import time

# readName='numberbatch-multi.txt'
# saveName='numberbatch-multi.bin'

readName='GoogleNews-vectors-negative300.bin'
saveName='google.bin'

print('Converting',readName,'to gensim model.')
init_load_time = time.time()

# For the CUMBERBATCH, it has to be binary=False
# model = KeyedVectors.load_word2vec_format(readName, binary=False)
model = KeyedVectors.load_word2vec_format(readName, binary=True)

print('Convertion complete in',(time.time() - init_load_time),'seconds.')

model.save(saveName)
