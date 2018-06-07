import extract_params as extr
import list_comparisions
import metrics.ssim
import metrics.psnr
import metrics.variance
import metrics.edges
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
    
    paramsDict[ "is_cropped" ] = False
    paramsDict[ "crop_x" ] = None
    paramsDict[ "crop_y" ] = None
    
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
def crop_image( tile_x, tile_y, tiles, image, reference ):

    width = image.width
    height = image.height
    
    if width != reference.width or height != reference.height:
        raise ValueError( 'Image and reference ahve different size.' )
        
    crop_width = width / tiles
    crop_height = height / tiles
    
    crop_x = tile_x * crop_width
    crop_y = tile_y * crop_height
    
    box = ( crop_x, crop_y, crop_x + crop_width, crop_y + crop_height )
    
    return ( image.crop( box ), reference.crop( box ) )
    
    
## ======================= ##
## 
def compare_images( reference_dir, compare_dir_parent, csv_file, features ):
    
    errors_list = []
    num_crops = 10      # In one dimmension
    
    compare_list = list_comparisions.list_all( reference_dir, compare_dir_parent )
    
    params = list( unique_params( compare_list ) )
    labels = list()

    labels.append( "reference_image" )
    labels.append( "image" )
    labels.append( "samples_reference" )
    
    labels.append( "is_cropped" )
    labels.append( "crop_x" )
    labels.append( "crop_y" )
    
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
                
                paramsDict = create_base_params_list( reference, to_compare )
                
                reference_image = Image.open( reference )
                image_to_compare = Image.open( to_compare )
                
                # Compute metrics for whole image
                metrics_dict = compute_metrics( reference_image, image_to_compare, features )
                paramsDict.update( metrics_dict )
                
                writer.writerow( paramsDict )
            
                # Compute metrics for crops
                for y in range( 0, num_crops ):
                    for x in range( 0, num_crops ):
                    
                        ( cropped_image, cropped_reference ) = crop_image( x, y, num_crops, image_to_compare, reference_image )
                
                        paramsDict[ "is_cropped" ] = True
                        paramsDict[ "crop_x" ] = x
                        paramsDict[ "crop_y" ] = y
                    
                        metrics_dict = compute_metrics( cropped_reference, cropped_image, features )
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
    
    features = [ metrics.ssim.MetricSSIM(), metrics.psnr.MetricPSNR(), metrics.variance.ImageVariance(), metrics.edges.MetricEdgeFactor() ]

    compare_images( reference_dir, compare_dir_parent, csv_file, features )
        
        
if __name__ == "__main__":
    run()
    