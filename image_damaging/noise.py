from PIL import Image, ImageMath
import sys
import os
import helpers
import numpy



## ======================= ##
##
def add_noise( image, noise ):

    ( image_r, image_g, image_b ) = image.split()
    
    noised_r = ImageMath.eval( "convert( a+b, 'L' )", a=image_r, b=noise )
    noised_g = ImageMath.eval( "convert( a+b, 'L' )", a=image_g, b=noise )
    noised_b = ImageMath.eval( "convert( a+b, 'L' )", a=image_b, b=noise )
    
    return Image.merge( 'RGB', ( noised_r, noised_g, noised_b ) )

## ======================= ##
##
def noise( image, parameters ):
    
    mean = parameters.mean
    stddev = parameters.stddev
    size = image.width * image.height
    
    random_noise = numpy.random.normal( mean, stddev, size )
    random_noise = numpy.reshape( random_noise, [ image.height, image.width ] )

    random_image = Image.fromarray( random_noise )

    return add_noise( image, random_image )

      
## ======================= ##
##
def param_to_postfix( parameters ):
    
    return "_noise_mean" + str( parameters.mean ) + "_stddev" + str( parameters.stddev )
      
## ======================= ##
##
def run():

    parameters = []
    
    stddevs = ( 3, 6, 9, 12, 15 )
    
    for stddev in stddevs:
        parameters_set = helpers.Parameters()
        
        parameters_set.mean = 0
        parameters_set.stddev = stddev
        parameters_set.file_postfix = param_to_postfix( parameters_set )
        
        parameters.append( parameters_set )

    helpers.simple_process_directory( sys.argv[ 1 ], sys.argv[ 2 ], noise, parameters )

    
    
if __name__ == "__main__":
    run()