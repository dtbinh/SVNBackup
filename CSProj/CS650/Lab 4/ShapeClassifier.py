'''
Created on 2014-11-2

@author: Walter
'''
import numpy as np
from kmean import *

class ShapeClassifier(object):

    def __init__(self, feature_dim, cluster_num):
        self.shapes = []
        self.feature_dim = feature_dim
        self.cluster_num = cluster_num

    def addShape(self, shape):
        self.shapes.append(shape)
        
    def classify(self):
        
        self.feature_vec = []
        self.shape_label = np.zeros(len(self.shapes), np.int)
        for s in self.shapes:
            self.feature_vec.append(s.getFeatureVector())
            
        # Normalize feature_vec
        featureVec = np.array(self.feature_vec)
        self.dimMax = featureVec.max(axis=0)
        self.dimMin = featureVec.min(axis=0)
        self.dimRange = self.dimMax - self.dimMin
        print "max " + str(self.dimMax)
        print "min " + str(self.dimMin)
        print "range " + str(self.dimRange)
        for f in self.feature_vec:
            for d in range(self.feature_dim):
                f[d] = (f[d] - self.dimMin[d]) / float(self.dimRange[d])
      
        self.km = KMeanCluster(self.feature_dim, self.cluster_num)
        self.km.cluster(self.feature_vec)
        
        for i in range(len(self.shapes)):
            dist, self.shape_label[i] = self.km.getLabel(self.feature_vec[i])
            self.shapes[i].label = self.shape_label[i]
            
    def getLabel(self, shape):
        feature_label = shape.getFeatureVector()
        for d in range(self.feature_dim):
            feature_label[d] = (feature_label[d] - self.dimMin[d]) / float(self.dimRange[d])
        dist, label = self.km.getLabel(feature_label)
        return label
            
    
        
            