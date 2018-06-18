import numpy
import sys
import os

import sklearn
from sklearn.externals import joblib


## ======================= ##
##
class DecisionTree:
    
    ## ======================= ##
    ##
    def __init__( self, clf ):
        self.clf = clf
        
    ## ======================= ##
    ##
    def load( file ):
    
        clf = joblib.load( file )
        return DecisionTree( clf )


    ## ======================= ##
    ##
    def train( samples, index_labels ):

        print( "Teaching decision tree." )
        clf = sklearn.tree.DecisionTreeClassifier()
        clf = clf.fit( samples, index_labels )
        
        return clf
        
    ## ======================= ##
    ##
    def train_and_save( samples, index_labels, file ):
        
        clf = DecisionTree.train( samples, index_labels )
        
        print( "Saving tree to file: " + file )
        joblib.dump( clf, file )
        
        return DecisionTree( clf )
        
    ## ======================= ##
    ##
    def classify( self, data_set, unique_labels ):
        
        return self.clf.predict( data_set )
        
        