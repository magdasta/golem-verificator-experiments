import sys
import math


max_reputation = 10



## ======================= ##
##
def increment_reputation_part( reputation_part ):

    return 1 + 0.9 * reputation_part


## ======================= ##
##
def compute_number_crops( reputation, max_crops = 3, new_nodes_distrust = 1 ):
    
    failed_timeout = reputation[ "failed_timeout" ]
    failed_verification = reputation[ "failed_verification" ]
    failed = reputation[ "failed" ]
    good = reputation[ "good" ]
    
    sum = failed_timeout + failed_verification + failed + good
    
    anti_reputation = failed_verification / sum
    history_len_coeff = 1 - sum / max_reputation
    
    print( "Anti reputation: " + str( anti_reputation ) )
    print( "History coeff: " + str( history_len_coeff ) )

    weighted_distrust = 3 * anti_reputation #+ new_nodes_distrust * history_len_coeff
    normalization_factor = 1
    
    print( "Weighted distrust " + str( weighted_distrust ) )
    
    weighted_distrust = math.sqrt( weighted_distrust / normalization_factor )
    
    print( "Weighted distrust exp " + str( weighted_distrust ) )
    
    range = math.sqrt( 3 )
    print( "Range: " + str( range ) )
    
    num_crops = weighted_distrust * max_crops / range
    print( "Not rounded crops: " + str( num_crops ) )
    
    return math.ceil( num_crops )


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
    