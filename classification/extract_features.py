import extract_params as extr
import list_comparisions
import metrics.ssim
import metrics.psnr
from PIL import Image

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
def create_base_params_list( reference, to_compare ):

    paramsDict = dict()
    paramsDict[ "reference_image" ] = reference
    paramsDict[ "image" ] = to_compare
    
    params_list = extr.extract_params( to_compare )
    reference_params_list = extr.extract_params( reference )
    
    paramsDict[ "samples_reference" ] = reference_params_list[ 0 ][ 1 ]
    
    for param in params_list:
        paramsDict[ param[ 0 ] ] = param[ 1 ]
        
    return paramsDict


## ======================= ##
## 
def compute_metrics( reference_image, image_to_compare, features ):
    
    paramsDict = dict()
    
    # Compute features
    for feature in features:
        metrics_dict = feature.compute_metrics( reference_image, image_to_compare )
        paramsDict.update( metrics_dict )
            
    return paramsDict
    
## ======================= ##
## 
def compare_images( reference_dir, compare_dir_parent, csv_file, features ):
    
    errors_list = []
    
    compare_list = list_comparisions.list_all( reference_dir, compare_dir_parent )
    
    params = list( unique_params( compare_list ) )
    labels = list()

    labels.append( "reference_image" )
    labels.append( "image" )
    labels.append( "samples_reference" )
    
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
            
            print( "Comparing images: " )
            print( "    [" + reference + "] and: ")
            print( "    [" + to_compare + "]")
        
            try:
                
                reference_image = Image.open( reference )
                image_to_compare = Image.open( to_compare )
            
                paramsDict = create_base_params_list( reference, to_compare )
            
                metrics_dict = compute_metrics( reference_image, image_to_compare, features )
                paramsDict.update( metrics_dict )
                
                writer.writerow( paramsDict )
            
            except Exception as e:
            
                print( "    Error: " )
                print( "        " + str( e ) )
                
                errors_list.append( ( reference, to_compare, str( e ) ) )
                
    if len( errors_list ) > 0:
    
        print( "\n## ===================================================== ##" )
        print( str( len( errors_list ) ) + " errors occured when processing following files:" )
        
        for error in errors_list:
            print( "    [" + error[ 0 ] + "] and [" + error[ 1 ] + "]" )
            print( "     Message: " + error[ 2 ] )
    else:
        print( "\n## ===================================================== ##" )
        print( "Processing completed without errors." )
    
## ======================= ##
##
def run():
    
    reference_dir = sys.argv[ 1 ]
    compare_dir_parent = sys.argv[ 2 ]
    csv_file = sys.argv[ 3 ]
    
    features = [ metrics.ssim.MetricSSIM(), metrics.psnr.MetricPSNR() ]

    compare_images( reference_dir, compare_dir_parent, csv_file, features )
        
        
if __name__ == "__main__":
    run()
    