import numpy
import sys
import os

from sklearn import tree
from sklearn.externals import joblib
import graphviz 
import pickle

import quality
import loading


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

    str_model = joblib.dump( clf, file )

    
## ======================= ##
##
def label_to_int( label, unique_labels ):
    return unique_labels.index( label )
    
  
## ======================= ##
##
def labels_to_int( data, label ):

    unique_labels = quality.compute_unique_labels( data, "label" )
    index_labels = [ label_to_int( label, unique_labels ) for label in data[ label ] ]
    
    return ( index_labels, unique_labels )
  
    
## ======================= ##
##
def run():

    data = loading.load_dataset( sys.argv[ 1 ] )
    data = data[ data[ "label" ] != b'IGNORE' ]
    data = data[ data[ "label" ] != b'DONT_KNOW' ]
    
    print( "Extracting labels data." )
    ( index_labels, unique_labels ) = labels_to_int( data, "label" )
    
    print( "Extracting features from dataset." )
    samples = data[ [ "ssim", "comp_edge_factor", "wavelet_mid", "wavelet_low", "wavelet_high" ] ]
    samples = samples.view( numpy.float64 ).reshape( samples.shape + (-1,) )
    
    print( "Teaching decision tree." )
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit( samples, index_labels )
    
    save_model( clf, sys.argv[ 2 ] )
    

if __name__ == "__main__":
    run()
