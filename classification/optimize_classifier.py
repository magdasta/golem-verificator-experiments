import sys
import loading

import matplotlib.pyplot

import quality
import teach_model
import data_analysis
import features as ft


## ======================= ##
##
def run():
    
    train_set = loading.load_dataset( sys.argv[ 1 ] )
    test_set = loading.load_dataset( sys.argv[ 2 ] )
    
    ( index_labels, unique_labels ) = teach_model.labels_to_int( train_set, "label" )
    
    features_labels = ft.get_train_feature_labels()
    
    correct_rejections = list()
    incorrect_rejections = list()
    
    weights = [ i * 10 + 1 for i in range( 0, 50 ) ]
    
    for weight in weights:
    
        params = teach_model.Parameters()
        params.classes_weights = dict()
        params.classes_weights[ b"TRUE" ] = weight
        params.classes_weights[ b"FALSE" ] = 1    
        params.criterion = "gini"
        params.max_depth = 7
        params.min_samples_leaf = 4000
        params.min_impurity_decrease = 0.0
        
        classifier = teach_model.teach_tree( train_set, features_labels, params, sys.argv[ 3 ] )

        ( error_matrix, unique_labels ) = quality.classification_quality( test_set, classifier, "label" )
        
        correct_rejections.append( quality.compute_correct_rejection_rate( error_matrix, unique_labels ) )
        incorrect_rejections.append( quality.compute_incorrect_rejection_rate( error_matrix, unique_labels ) )
        
    #data_analysis.show_multidata( correct_rejections,  )
    print( correct_rejections )
    print( incorrect_rejections )

    matplotlib.pyplot.plot( weights, correct_rejections )
    matplotlib.pyplot.plot( weights, incorrect_rejections )

    matplotlib.pyplot.xlabel( "TRUE label weight" )
    matplotlib.pyplot.ylabel( "Quality" )
    
    matplotlib.pyplot.show()


if __name__ == "__main__":
    run()
