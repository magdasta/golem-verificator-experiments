import sys
import math

import numpy
from sklearn.externals import joblib

import quality
import loading
import classifiers.decision_tree
import manual_labeling
import features as ft



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
def teach_tree( data, features_labels, params, file ):

    print( "Extracting labels data." )
    ( index_labels, unique_labels ) = labels_to_int( data, "label" )
    
    print( "Filtering data." )
    data, index_labels = filter_ignores( data, index_labels )
    data, index_labels = filter_dontknows( data, index_labels )

    clf = classifiers.decision_tree.DecisionTree.train_and_save( data, "label", features_labels, params, file )
    return clf

  
## ======================= ##
##
def run():

    data = loading.load_dataset( sys.argv[ 1 ] )
    data = data[ data[ "is_cropped" ] == True ]
    
    ( index_labels, unique_labels ) = labels_to_int( data, "label" )
    
    features_labels = [
        "ssim", "psnr", "max_x_mass_center_distance", "histograms_correlation",
        "max_y_mass_center_distance", "edge_difference", "comp_edge_factor",
        "wavelet_mid", "wavelet_low", "wavelet_high",
        "wavelet_sym2_base", "wavelet_sym2_low", "wavelet_sym2_mid", "wavelet_sym2_high",
        "wavelet_db4_base", "wavelet_db4_low", "wavelet_db4_mid", "wavelet_db4_high",
        "wavelet_haar_base", "wavelet_haar_low", "wavelet_haar_mid", "wavelet_haar_high",
        "wavelet_haar_freq_x1", "wavelet_haar_freq_x2", "wavelet_haar_freq_x3"
        ]

    
    params = dict()
    params[ "criterion" ] = "gini"
    params[ "splitter" ] = "best"
    params[ "max_depth" ] = 8
    params[ "min_samples_leaf" ] = 3000
    params[ "min_impurity_decrease" ] = 0.0
    
    params[ "classes_weights" ] = dict()
    params[ "classes_weights" ][ b"TRUE" ] = 10
    params[ "classes_weights" ][ b"FALSE" ] = 1
    
    print( "Teaching: number True labels: " + str( len( data[ data[ "label" ] == b"TRUE" ] ) ) )
    print( "Teaching: number False labels: " + str( len( data[ data[ "label" ] == b"FALSE" ] ) ) )
    
    clf = teach_tree( data, features_labels, params, sys.argv[ 2 ] )
    clf.save_graph( sys.argv[ 3 ] )
    
    clf.print_info()
    

if __name__ == "__main__":
    run()
