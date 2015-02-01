from __future__ import division, unicode_literals
import math
from textblob import TextBlob as tb

import cPickle as pickle
import numpy as np
import scipy.spatial as spa

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

def Track(stuff):
    return str(stuff)

titles = []
tit_dict = {}

bloblist = []
meaninglist = []
spotifys = []

tfidfs = []

distances = []

i=0
for line in open('db.txt','r'):
    content = line.split("%DIV%")
    title = content[0]
    other = eval(content[1])
    bloblist.append(tb(other[0]))
    meaninglist.append(tb(other[1]))
    spotifys.append(other[2])
    tit_dict[title] = i
    i +=1

#done getting raw processed data
for i, blob in enumerate(meaninglist):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    my_dict = {}
    for word, score in sorted_words:
        my_dict[word] = score
    tfidfs.append(my_dict)
    

for song in tfidfs:
    my_words =  set(song.keys())
    my_distances = []
    for song2 in tfidfs:
        his_words = set(song2.keys())
        intersection = my_words & his_words
        mine = np.array(sorted( [ my_words[co] for co in intersection] ))
        his = np.array(sorted( [ his_words[co] for co in intersection] ))
        diff = spa.distance.cosine(mine,his)
        my_distances.append(diff)
    distances.append(my_distances)

print('yay')

with open('distances.pickle', 'wb') as d:
    pickle.dump(distances,d,protocol=pickle.HIGHEST_PROTOCOL)

with open('spotifys.pickle', 'wb') as s:
    pickle.dump(spotifys,s,protocol=pickle.HIGHEST_PROTOCOL)
        
with open('titles.pickle', 'wb') as t:
    pickle.dump(titles,t,protocol=pickle.HIGHEST_PROTOCOL)
        
with open('tit_dic.pickle', 'wb') as dd:
    pickle.dump(tit_dict,dd,protocol=pickle.HIGHEST_PROTOCOL)
