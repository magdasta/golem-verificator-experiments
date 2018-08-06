import numpy
import sys
import os
import math

import loading

import classifiers.decision_tree




## ======================= ##
##
def run():

    classifier = classifiers.decision_tree.DecisionTree.load( sys.argv[ 1 ] )
    classifier.print_info()
    
    
if __name__ == "__main__":
    run()
    
    