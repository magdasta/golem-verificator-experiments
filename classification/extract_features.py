import extract_params as extr
import list_comparisions

import sys
import csv


## ======================= ##
##
def unique_params( compare_list ):

    labels = set()

    for ( reference, to_compare ) in compare_list:
        
        params_list = extr.extract_params( to_compare )
        for param in params_list:
            labels.add( param[ 0 ] )

    return labels

    
## ======================= ##
## 
def compare_images( reference_dir, compare_dir_parent, csv_file ):
    
    compare_list = list_comparisions.list_all( reference_dir, compare_dir_parent )
    
    params = list( unique_params( compare_list ) )
    labels = list()

    labels.append( "reference_image" )
    labels.append( "image" )
    
    labels = labels + params
    
    print( "Parameters that will be written to csv file: " + str( params ) )

    with open( csv_file, 'w', newline='') as csvfile:

        writer = csv.DictWriter( csvfile, fieldnames = labels )
        writer.writeheader()
        
        for ( reference, to_compare ) in compare_list:
            
            paramsDict = dict()
            paramsDict[ "reference_image" ] = reference
            paramsDict[ "image" ] = to_compare
            
            params_list = extr.extract_params( to_compare )
            
            for param in params_list:
                paramsDict[ param[ 0 ] ] = param[ 1 ]
        
            writer.writerow( paramsDict )
    
    
reference_dir = sys.argv[ 1 ]
compare_dir_parent = sys.argv[ 2 ]
csv_file = sys.argv[ 3 ]

compare_images( reference_dir, compare_dir_parent, csv_file )
        
    