import loading
import sys

import classifiers.decision_tree

import data_analysis
import features as ft


## ======================= ##
##
def run():

    classifier = classifiers.decision_tree.DecisionTree.load( sys.argv[ 2 ] )
    classifier.set_features_labels( ft.get_feature_labels() )
    
    data = loading.load_dataset( sys.argv[ 1 ] )
    results = classifier.classify( data )
    
    result_mask = ( results[:] == b"TRUE" ) & ( data[ "label" ] == b"FALSE" )
    filtered_data = data[ result_mask ]
    
    data_analysis.save_filtered_dataset( filtered_data, sys.argv[ 3 ], sys.argv[ 4 ] )
    
    
if __name__ == "__main__":
    run()
    
    