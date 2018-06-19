import numpy

from sklearn import tree
from sklearn.externals import joblib
from sklearn.externals.six import StringIO
import pydot


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
    def set_features_labels( self, labels ):
    
        self.labels = labels
        
    ## ======================= ##
    ##
    def save_graph( self, file ):
        
        print( "Saving tree to file [" + file + "]" )
        
        dot_data = StringIO() 
        tree.export_graphviz( self.clf, out_file=dot_data, feature_names = self.labels, rounded = True, filled = True ) 
        graph = pydot.graph_from_dot_data( dot_data.getvalue() )
        graph[ 0 ].write_pdf( file ) 
        
        
    ## ======================= ##
    ##
    def train( samples, index_labels, params ):

        print( "Teaching decision tree." )
        clf = tree.DecisionTreeClassifier()
        clf.max_depth = 5
        clf.class_weight = params.classes_weights
        
        clf = clf.fit( samples, index_labels )
        
        return clf

    ## ======================= ##
    ##
    def extract_features( data, labels ):
    
        print( "Extracting features from dataset." )
        samples = data[ labels ]
        return samples.view( numpy.float64 ).reshape( samples.shape + (-1,) )
        
    ## ======================= ##
    ##
    def train_and_save( data, index_labels, features_labels, params, file ):
        
        samples = DecisionTree.extract_features( data, features_labels )
        clf = DecisionTree.train( samples, index_labels, params )
        
        print( "Saving tree to file: " + file )
        joblib.dump( clf, file )
        
        decision_tree = DecisionTree( clf )
        decision_tree.set_features_labels( features_labels )
        
        return decision_tree
        
        
    ## ======================= ##
    ##
    def classify( self, data_set, unique_labels ):
        
        samples = data_set[ self.labels ]
        samples = samples.view( numpy.float64 ).reshape( samples.shape + (-1,) )
        
        results = self.clf.predict( samples )
        results = [ unique_labels[ label ] for label in results ]
        
        return numpy.array( results )
        
        
        