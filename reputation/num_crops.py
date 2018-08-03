import sys
import math
import numpy


max_reputation = 10



## ======================= ##
##
def compute_number_crops( reputation, max_crops = 3, new_nodes_distrust = 1 ):
    
    failed_timeout = reputation[ "failed_timeout" ]
    failed_verification = reputation[ "failed_verification" ]
    failed = reputation[ "failed" ]
    good = reputation[ "good" ]
    
    sum = failed_timeout + failed_verification + failed + good
    
    anti_reputation = 0
    if sum > 10:
        raise ValueError( "Sum of reputation coefficients exceeds maximal value = 10." )
    if sum != 0:
        anti_reputation = failed_verification / sum
        
    weighted_distrust = math.sqrt( 3 * anti_reputation )
    
    range = math.sqrt( 3 )
    num_crops = weighted_distrust * max_crops / range
    
    return numpy.clip( math.ceil( num_crops ), 1, max_crops )


## ======================= ##
##
def run():
    
    reputation = dict()
    reputation[ "failed_timeout" ] = float( sys.argv[ 1 ] )
    reputation[ "failed_verification" ] = float( sys.argv[ 2 ] )
    reputation[ "failed" ] = float( sys.argv[ 3 ] )
    reputation[ "good" ] = float( sys.argv[ 4 ] )
    
    
    num_crops = compute_number_crops( reputation )
    print( num_crops )
        
        
if __name__ == "__main__":
    run()
    