import os
import sys
import traceback
import csv

from PIL import Image

import extract_params as extr
import list_comparisions
import golem_verificator.docker.blender.images.scripts.metrics.ssim
import golem_verificator.docker.blender.images.scripts.metrics.psnr
import golem_verificator.docker.blender.images.scripts.metrics.variance
import golem_verificator.docker.blender.images.scripts.metrics.edges
import golem_verificator.docker.blender.images.scripts.metrics.wavelet
import golem_verificator.docker.blender.images.scripts.metrics.histograms_correlation
import golem_verificator.docker.blender.images.scripts.metrics.mass_center_distance
import features as ft

import data_filtering


## ======================= ##
##
def create_directory_if_doesnt_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)

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
def compare_images( reference_dir, compare_dir_parent, csv_file, features, scenes ):
    
    create_directory_if_doesnt_exist( os.path.dirname( csv_file ) )
    
    errors_list = []
    num_crops = 10      # In one dimmension
    
    compare_list = list_comparisions.list_all( reference_dir, compare_dir_parent, scenes )
    
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
                
                errors_list.append( ( reference, to_compare, str( e ), traceback.format_exc() ) )
                
    if len( errors_list ) > 0:
    
        print( "\n## ===================================================== ##" )
        print( str( len( errors_list ) ) + " errors occured when processing following files:" )
        
        for error in errors_list:
            print( "    [" + error[ 0 ] + "] and [" + error[ 1 ] + "]" )
            print( "     Message: " + error[ 2 ] )
            print( error[ 3 ] )
    else:
        print( "\n## ===================================================== ##" )
        print( "Processing completed without errors." )

## ======================= ##
##
def convert_to_npy( csv_file ):

    print( "Converting .csv to binary file." )
    
    ( file, ext ) = os.path.splitext( csv_file )
    npy_file = file + ".npy"

    data_filtering.convert_to_binary( csv_file, npy_file )

        
## ======================= ##
##
def run():
    
    reference_dir = sys.argv[ 1 ]
    compare_dir_parent = sys.argv[ 2 ]
    csv_file = sys.argv[ 3 ]
    scenes = sys.argv[ 4: ]
    
    features = [    metrics.ssim.MetricSSIM,
                    metrics.psnr.MetricPSNR,
                    metrics.variance.ImageVariance,
                    metrics.edges.MetricEdgeFactor,
                    metrics.wavelet.MetricWavelet,
                    metrics.histograms_correlation.MetricHistogramsCorrelation,
                    metrics.mass_center_distance.MetricMassCenterDistance  ]

    ft.save_all_feature_labels(features)
    compare_images( reference_dir, compare_dir_parent, csv_file, features, scenes )
    
    convert_to_npy( csv_file )
        
        
if __name__ == "__main__":
    run()
    