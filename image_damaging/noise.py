from PIL import Image, ImageFilter
import sys
import os
import helpers
import numpy






## ======================= ##
##
def noise( image, parameters ):
    
    mean = parameters.mean
    stddev = parameters.stddev
    size = image.width * image.height
    
    random_noise = numpy.random.normal( mean, stddev, size )
    random_noise = numpy.reshape( random_noise, [ image.height, image.width ] )
    
    random_image = Image.fromarray( random_noise.astype( 'uint8' ) )
    random_image = Image.merge( 'RGB', ( random_image, random_image, random_image ) )
    
    return Image.blend( image, random_image, 0.1 )

      
## ======================= ##
##
def run():

    parameters = []
    parameters_set = helpers.Parameters()
    
    parameters_set.mean = 0
    parameters_set.stddev = 5
    parameters_set.file_postfix = "_noise_mean0_stddev5"
    
    parameters.append( parameters_set )

    helpers.simple_process_directory( sys.argv[ 1 ], sys.argv[ 2 ], noise, parameters )

    
    
if __name__ == "__main__":
    run()