import sys
import math


max_reputation = 10

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

    weighted_distrust = anti_reputation + new_nodes_distrust * history_len_coeff + new_nodes_distrust * anti_reputation * history_len_coeff
    normalization_factor = ( 1 + new_nodes_distrust + new_nodes_distrust ) / 3
    
    weighted_distrust = math.exp( weighted_distrust / normalization_factor )
    
    max_value = math.exp( 3 )
    
    return math.ceil( weighted_distrust * max_crops / max_value )


## ======================= ##
##
def run():
    


        
        
if __name__ == "__main__":
    run()
    