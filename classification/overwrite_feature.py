import os
import sys
import traceback
import csv
import math
import numpy

from PIL import Image

import extract_params as extr
import list_comparisions
import metrics.ssim
import metrics.psnr
import metrics.variance
import metrics.edges
import metrics.wavelet
import metrics.histograms_correlation
import metrics.mass_center_distance
import features as ft

import data_filtering
import extract_features
import loading


## ======================= ##
##
def compute_metrics_list( metrics_dict ):
    
    metrics_list = list()
    for metric, features in metrics_dict.items():
        metrics_list.append( metric )
        
    return metrics_list

## ======================= ##
##
def select_metrics_features( metrics, features ):

    metrics_dict = dict()
    
    for metric in metrics:
    
        features_list = list()
        
        labels = metric.get_labels()
        for label in labels:
            if label in features:
                features_list.append( label )
        
        if len( features_list ) > 0:
            metrics_dict[ metric ] = features_list
        
    return metrics_dict

## ======================= ##
##
def overwrite_features_impl( data, metrics_dict ):
    
    errors_list = []
    num_crops = 10      # In one dimmension
    
    print( "Selected features: " )
    for metric, features in metrics_dict.items():
        for feature in features:
            print( feature )
    
    metrics_list = compute_metrics_list( metrics_dict )
    
    reference_file = ""
    compared_file = ""
    
    reference_image = None
    image_to_compare = None
    
    for row in data:
        
        if reference_file != row[ "reference_image" ].decode('UTF-8') and compared_file != row[ "image" ].decode('UTF-8'):
        
            reference_file = row[ "reference_image" ].decode('UTF-8')
            compared_file = row[ "image" ].decode('UTF-8')
            
            print( "Overwriting features for images: " )
            print( "    [" + reference_file + "] and: ")
            print( "    [" + compared_file + "]")

            reference_image = Image.open( reference_file )
            image_to_compare = Image.open( compared_file )
        
        try:
        
            features_dict = None
            if row[ "is_cropped" ]:
                
                ( cropped_image, cropped_reference ) = extract_features.crop_image( row[ "crop_x" ], row[ "crop_y" ], num_crops, image_to_compare, reference_image )
                features_dict = extract_features.compute_metrics( cropped_reference, cropped_image, metrics_list )
            else:
                features_dict = extract_features.compute_metrics( reference_image, image_to_compare, metrics_list )
                
            for feature_name, value in features_dict.items():
                row[ feature_name ] = value

        except Exception as e:
        
            print( "    Error: " )
            print( "        " + str( e ) )
            
            errors_list.append( ( reference_file, compared_file, str( e ), traceback.format_exc() ) )
            
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
        
    return data
    
## ======================= ##
##
def overwrite_features( data, metrics, features ):

    metrics_dict = select_metrics_features( metrics, features )
    return overwrite_features_impl( data, metrics_dict )

    
resolutions = {
    b"atom" : [ 1280, 720 ],
    b"barcelona" : [ 800, 600 ],
    b"breakfast_room" : [ 800, 600 ],
    b"bunkbed" : [ 800, 600 ],
    b"car" : [ 1600, 1200 ],
    b"cat" : [ 1600, 1200 ],
    b"eco_light_bulb" : [ 800, 600 ],
    b"french_woman" : [ 1920, 1080 ],
    b"glass" : [ 800, 600 ],
    b"glass_material" : [ 800, 600 ],
    b"habitacion" : [ 800, 600 ],
    b"head" : [ 600, 450 ],
    b"interior" : [ 1497, 865 ],
    b"metal" : [ 800, 600 ],
    b"mug" : [ 800, 600 ],
    b"office" : [ 800, 600 ],
    b"plushy" : [ 400, 300 ],
    b"ring" : [ 800, 600 ],
    b"rocks" : [ 1920, 1080 ],
    b"sea" : [ 800, 600 ],
    b"shark" : [ 1920, 1080 ],
    b"toughship" : [ 800, 600 ],
    b"tree" : [ 800, 600 ]
}

    
## ======================= ##
##
def fix_psnr_infs( data ):
    
    for row in data:
        if math.isinf( row[ "psnr" ] ):
            row[ "psnr" ] = numpy.finfo( numpy.float32 ).max
        
## ======================= ##
##
def rescale_wavelets_to_resolution( data, crop_divisor ):
    
    for row in data:
        
        resolution = resolutions[ row[ "scene" ] ]
        rescale = 1 / ( resolution[ 0 ] * resolution[ 1 ] )
        if row[ "is_cropped" ]:
            rescale = crop_divisor * crop_divisor * rescale
        
        row[ "wavelet_sym2_base" ] = row[ "wavelet_sym2_base" ] * rescale
        row[ "wavelet_db4_base" ] = row[ "wavelet_db4_base" ] * rescale
        row[ "wavelet_haar_base" ] = row[ "wavelet_haar_base" ] * rescale

## ======================= ##
##
def run():
    
    data_file = sys.argv[ 1 ]
    target_file = sys.argv[ 2 ]
    features = sys.argv[ 3: ]
    
    data = loading.load_dataset( data_file )
    
    
    metrics_obj = [    metrics.ssim.MetricSSIM,
                    metrics.psnr.MetricPSNR,
                    metrics.variance.ImageVariance,
                    metrics.edges.MetricEdgeFactor,
                    metrics.wavelet.MetricWavelet,
                    metrics.histograms_correlation.MetricHistogramsCorrelation,
                    metrics.mass_center_distance.MetricMassCenterDistance  ]

                    
    #fix_psnr_infs( data )
    #rescale_wavelets_to_resolution( data, 13 )

                    
    data = overwrite_features( data, metrics_obj, features )
    
    loading.save_binary( data, target_file )
        
        
if __name__ == "__main__":
    run()
