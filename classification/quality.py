import numpy
import sys
import os

import data_analysis
import loading

import classifiers.ssim_threshold

    

## ======================= ##
##
def compute_error_matrix( results, expected, unique_labels ):

    matrix_size = len( unique_labels )
    error_matrix = numpy.zeros( ( matrix_size, matrix_size ) )
    
    for expected_label_idx in range( 0, matrix_size ):
    
        expected_mask = expected[ : ] == unique_labels[ expected_label_idx ]
    
        for real_label_idx in range( 0, matrix_size ):
            
            real_results = results[ expected_mask ]
            same_results = [ real_result for real_result in real_results if real_result == unique_labels[ real_label_idx ] ]
            
            error_matrix[ expected_label_idx ][ real_label_idx ] = len( same_results )
    
    return error_matrix
    
    
## ======================= ##
##
def compute_unique_labels( data_set, label ):

    unique_labels = set( data_set[ label ] )
    return list( unique_labels )

## ======================= ##
##
def compute_expected_results( data_set, unique_labels, label ):
    
    expected = data_set[ label ]
    
    return expected
    
    
## ======================= ##
##
def classification_quality( data_set, classifier, label ):

    unique_labels = compute_unique_labels( data_set, label )
    
    results = classifier.classify( data_set, unique_labels )
    expected = compute_expected_results( data_set, unique_labels, label )
    
    return ( compute_error_matrix( results, expected, unique_labels ), unique_labels )


## ======================= ##
##
def print_classification_results( error_matrix, unique_labels ):

    print( unique_labels )
    print( error_matrix )
    
    
    
## ======================= ##
##
def load_and_classify( data_file, classifier, label ):
    
    data = loading.load_dataset( data_file )
    ( error_matrix, unique_labels ) = classification_quality( data, classifier, label )
    
    print_classification_results( error_matrix, unique_labels )

    
    
## ======================= ##
##
def run():

    classifier = classifiers.ssim_threshold.ThresholdSSIM( 0.92 )
    
    load_and_classify( sys.argv[ 1 ], classifier, "label" )
    

if __name__ == "__main__":
    run()

    
