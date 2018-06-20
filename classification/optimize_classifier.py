import quality
import teach_model
import data_analysis
import loading

import matplotlib.pyplot

import sys




## ======================= ##
##
def run():
    
    train_set = loading.load_dataset( sys.argv[ 1 ] )
    test_set = loading.load_dataset( sys.argv[ 2 ] )
    
    ( index_labels, unique_labels ) = teach_model.labels_to_int( train_set, "label" )
    
    features_labels = [ "ssim", "comp_edge_factor", "wavelet_mid", "wavelet_low", "wavelet_high" ]
    
    correct_rejections = list()
    incorrect_rejections = list()
    
    for i in range( 0, 50 ):
    
        params = teach_model.Parameters()
        params.classes_weights = dict()
        params.classes_weights[ b"TRUE" ] = i * 10 + 1
        params.classes_weights[ b"FALSE" ] = 1    
        params.criterion = "entropy"
        params.max_depth = 5
        
        classifier = teach_model.teach_tree( train_set, features_labels, params, sys.argv[ 3 ] )

        ( error_matrix, unique_labels ) = quality.classification_quality( test_set, classifier, "label" )
        
        correct_rejections.append( quality.compute_correct_rejection_rate( error_matrix, unique_labels ) )
        incorrect_rejections.append( quality.compute_incorrect_rejection_rate( error_matrix, unique_labels ) )
        
    #data_analysis.show_multidata( correct_rejections,  )
    print( correct_rejections )
    print( incorrect_rejections )

    matplotlib.pyplot.plot( correct_rejections, incorrect_rejections )

    matplotlib.pyplot.xlabel( "False rejections rate" )
    matplotlib.pyplot.ylabel( "Correct rejections rate" )
    
    matplotlib.pyplot.show()


if __name__ == "__main__":
    run()
