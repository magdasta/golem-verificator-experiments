import numpy
import sys
import os

from sklearn import tree
from sklearn.externals import joblib
import graphviz 
import pickle


import quality
import loading
import classifiers.decision_tree



## ======================= ##
##
class Parameters:
    pass


## ======================= ##
##
def save_model( clf, file ):

    joblib.dump( clf, file )

    
## ======================= ##
##
def label_to_int( label, unique_labels ):
    return unique_labels.index( label )
    
  
## ======================= ##
##
def labels_to_int( data, label ):

    unique_labels = quality.compute_unique_labels( data, "label" )
    index_labels = numpy.array( [ label_to_int( label, unique_labels ) for label in data[ label ] ] )
    
    return ( index_labels, unique_labels )
  
## ======================= ##
##
def filter_ignores( data, indexed_labels ):

    filter_mask = data[ "label" ] != b'IGNORE'
    
    data = data[ filter_mask ]
    indexed_labels = indexed_labels[ filter_mask ]
    
    return data, indexed_labels
    
## ======================= ##
##
def filter_dontknows( data, indexed_labels ):

    filter_mask = data[ "label" ] != b'DONT_KNOW'

    data = data[ filter_mask ]
    indexed_labels = indexed_labels[ filter_mask ]
    
    return data, indexed_labels
  
    
## ======================= ##
##
def run():

    data = loading.load_dataset( sys.argv[ 1 ] )
    
    print( "Extracting labels data." )
    ( index_labels, unique_labels ) = labels_to_int( data, "label" )
    
    print( "Filtering data." )
    data, index_labels = filter_ignores( data, index_labels )
    data, index_labels = filter_dontknows( data, index_labels )

    features_labels = [ "ssim", "comp_edge_factor", "wavelet_mid", "wavelet_low", "wavelet_high" ] 
    
    params = Parameters()
    params.classes_weights = dict()
    params.classes_weights[ unique_labels.index( b"TRUE" ) ] = 0.8
    params.classes_weights[ unique_labels.index( b"FALSE" ) ] = 0.2
    params.classes_weights[ unique_labels.index( b"DONT_KNOW" ) ] = 0.0
    params.classes_weights[ unique_labels.index( b"IGNORE" ) ] = 0.0
    
    
    clf = classifiers.decision_tree.DecisionTree.train_and_save( data, index_labels, features_labels, params, sys.argv[ 2 ] )
    clf.save_graph( sys.argv[ 3 ] )
    

if __name__ == "__main__":
    run()
