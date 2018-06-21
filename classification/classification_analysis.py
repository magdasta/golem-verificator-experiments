import classifiers.decision_tree
import data_analysis
import loading



import sys





## ======================= ##
##
def run():

    classifier = classifiers.decision_tree.DecisionTree.load( sys.argv[ 2 ] )
    classifier.set_features_labels( [ "ssim", "comp_edge_factor", "wavelet_mid", "wavelet_low", "wavelet_high" ] )
    
    data = loading.load_dataset( sys.argv[ 1 ] )
    results = classifier.classify( data )
    
    result_mask = ( results[:] == b"TRUE" ) & ( data[ "label" ] == b"FALSE" )
    filtered_data = data[ result_mask ]
    
    data_analysis.save_filtered_dataset( filtered_data, sys.argv[ 3 ], sys.argv[ 4 ] )
    
    
    

if __name__ == "__main__":
    run()
    
    