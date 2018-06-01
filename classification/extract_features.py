import extract_params as extr
import list_comparisions
import metrics.ssim

import os
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
def compare_images( reference_dir, compare_dir_parent, csv_file, features ):
    
    compare_list = list_comparisions.list_all( reference_dir, compare_dir_parent )
    
    params = list( unique_params( compare_list ) )
    labels = list()

    labels.append( "reference_image" )
    labels.append( "image" )
    
    labels = labels + params
    
    for feature in features:
        labels = labels + feature.get_labels()
    
    print( "\n## ===================================================== ##" )
    print( "Labels that will be written to csv file: " + str( labels ) )

    with open( csv_file, 'w', newline='') as csvfile:

        writer = csv.DictWriter( csvfile, fieldnames = labels )
        writer.writeheader()
        
        print( "\n## ===================================================== ##" )
        print( "Comparing images and computing metrics." )
        
        for ( reference, to_compare ) in compare_list:
            
            paramsDict = dict()
            paramsDict[ "reference_image" ] = reference
            paramsDict[ "image" ] = to_compare
            
            params_list = extr.extract_params( to_compare )
            
            for param in params_list:
                paramsDict[ param[ 0 ] ] = param[ 1 ]
        
            print( "Comparing images: " )
            print( "    [" + reference + "] and: ")
            print( "    [" + to_compare + "]")
        
            # Compute features
            for feature in features:
                metrics_dict = feature.compute_metrics( os.path.join( reference_dir, reference ), os.path.join( compare_dir_parent, to_compare ) )
                paramsDict.update( metrics_dict )
        
            writer.writerow( paramsDict )
    
    
## ======================= ##
##
def run():
    
    reference_dir = sys.argv[ 1 ]
    compare_dir_parent = sys.argv[ 2 ]
    csv_file = sys.argv[ 3 ]
    
    features = [ metrics.ssim.MetricSSIM() ]

    compare_images( reference_dir, compare_dir_parent, csv_file, features )
        
        
if __name__ == "__main__":
    run()
    