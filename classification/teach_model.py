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
def save_graph( clf, file ):
    
    print( "Saving tree to file [" + file + "]" )
    
    dot_data = tree.export_graphviz( clf, out_file=None ) 
    graph = graphviz.Source( dot_data ) 
    graph.render( file ) 

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
    
    print( "Extracting features from dataset." )
    samples = data[ [ "ssim", "comp_edge_factor", "wavelet_mid", "wavelet_low", "wavelet_high" ] ]
    samples = samples.view( numpy.float64 ).reshape( samples.shape + (-1,) )
    
    classifiers.decision_tree.DecisionTree.train_and_save( samples, index_labels, sys.argv[ 2 ] )
    

if __name__ == "__main__":
    run()
