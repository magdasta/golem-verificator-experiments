import extract_params as extr
import list_comparisions

import sys


## ======================= ##
##
def unique_params( compare_list ):

    labels = set()

    for ( reference, to_compare ) in compare_list:
        
        params_list = extr.extract_params( to_compare )
        for param in params_list:
            labels.add( param[ 0 ] )

    return labels

    
    
reference_dir = sys.argv[ 1 ]
compare_dir_parent = sys.argv[ 2 ]

compare_list = list_comparisions.list_all( reference_dir, compare_dir_parent )
params = unique_params( compare_list )

print( params )
