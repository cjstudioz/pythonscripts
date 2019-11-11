# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 22:00:50 2019

@author: c-ChunL
"""

import numpy as np
import sklearn.cluster
from fuzzywuzzy import fuzz, process
import nltk

words = [
    'my cat is black',        
    'my cat is white',        
    'my dog is black',
    'alan aint black',
    'jane aint blue', 
    'blue is jane',       
]
words = np.asarray(words) #So that indexing with a list will work
lev_similarity = -1*np.array([[nltk.edit_distance(w1,w2) for w1 in words] for w2 in words])

affprop = sklearn.cluster.AffinityPropagation(affinity="euclidean", damping=0.5, preference=-150.0, verbose=True)
affprop.fit(lev_similarity)


for cluster_id in np.unique(affprop.labels_):
    exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
    cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
    cluster_str = ", ".join(cluster)
    print(" - *%s:* %s" % (exemplar, cluster_str))
