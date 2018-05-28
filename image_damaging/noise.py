from PIL import Image, ImageMath
import sys
import os
import helpers
import numpy



## ======================= ##
##
def add_noise( image, noise_r, noise_g, noise_b ):

    channels = image.split()
    
    noised_r = ImageMath.eval( "convert( a+b, 'L' )", a=channels[ 0 ], b=noise_r )
    noised_g = ImageMath.eval( "convert( a+b, 'L' )", a=channels[ 1 ], b=noise_g )
    noised_b = ImageMath.eval( "convert( a+b, 'L' )", a=channels[ 2 ], b=noise_b )
    
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

    return add_noise( image, random_image, random_image, random_image )

## ======================= ##
##
def colored_noise( image, parameters ):

    mean = parameters.mean
    stddev = parameters.stddev
    size = image.width * image.height
    
    random_noise_r = numpy.random.normal( mean, stddev, size )
    random_noise_r = numpy.reshape( random_noise_r, [ image.height, image.width ] )

    random_noise_g = numpy.random.normal( mean, stddev, size )
    random_noise_g = numpy.reshape( random_noise_g, [ image.height, image.width ] )
    
    random_noise_b = numpy.random.normal( mean, stddev, size )
    random_noise_b = numpy.reshape( random_noise_b, [ image.height, image.width ] )
    
    random_image_r = Image.fromarray( random_noise_r )
    random_image_g = Image.fromarray( random_noise_g )
    random_image_b = Image.fromarray( random_noise_b )
    
    return add_noise( image, random_image_r, random_image_g, random_image_b )
    
    
      
## ======================= ##
##
def param_to_postfix( parameters ):
    
    return "_mean" + str( parameters.mean ) + "_stddev" + str( parameters.stddev )
      
## ======================= ##
##
def run():

    parameters = []
    
    stddevs = ( 3, 6, 9, 12, 15 )
    
    for stddev in stddevs:
        parameters_set = helpers.Parameters()
        
        parameters_set.mean = 0
        parameters_set.stddev = stddev
        parameters_set.file_postfix = "_noise" + param_to_postfix( parameters_set )
        
        parameters.append( parameters_set )

    #helpers.simple_process_directory( sys.argv[ 1 ], sys.argv[ 2 ], noise, parameters )
    
    for param_set in parameters:
        param_set.file_postfix = "_noise_colored" + param_to_postfix( param_set )
    
    
    helpers.simple_process_directory( sys.argv[ 1 ], sys.argv[ 2 ], colored_noise, parameters )

    
    
if __name__ == "__main__":
    run()