from PIL import Image, ImageMath
import sys
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
def burned_pixels( image, parameters ):
    
    mean = parameters.mean
    stddev = parameters.stddev
    size = image.width * image.height
    channel_probability = parameters.probability / 3
    
    random_noise = numpy.random.normal( mean, stddev, size )
    
    pixel_mask = numpy.random.rand( size )
    
    pixel_mask_r = ( pixel_mask < channel_probability )
    
    pixel_mask_g = ( pixel_mask < 2 * channel_probability )
    pixel_mask_g = ( pixel_mask >= channel_probability ) & pixel_mask_g
    
    pixel_mask_b = ( pixel_mask < 3 * channel_probability )
    pixel_mask_b = ( pixel_mask >= 2 * channel_probability ) & pixel_mask_b
    
    random_noise_r = random_noise * pixel_mask_r
    random_noise_r = numpy.reshape( random_noise_r, [ image.height, image.width ] )

    random_noise_g = random_noise * pixel_mask_g
    random_noise_g = numpy.reshape( random_noise_g, [ image.height, image.width ] )
    
    random_noise_b = random_noise * pixel_mask_b
    random_noise_b = numpy.reshape( random_noise_b, [ image.height, image.width ] )
    
    random_image_r = Image.fromarray( random_noise_r )
    random_image_g = Image.fromarray( random_noise_g )
    random_image_b = Image.fromarray( random_noise_b )

    return add_noise( image, random_image_r, random_image_g, random_image_b )
      
## ======================= ##
##
def param_to_postfix( parameters ):
    
    return "_[mean=" + str( parameters.mean ) + "]_[stddev=" + str( parameters.stddev ) + "]"
      
## ======================= ##
##
def run():

    parameters = []
    
    stddevs = ( 3, 6, 9, 12, 15 )
    
    for stddev in stddevs:
        parameters_set = helpers.Parameters()
        
        parameters_set.mean = 0
        parameters_set.stddev = stddev
        parameters_set.file_postfix = "_[noise]" + param_to_postfix( parameters_set )
        
        parameters.append( parameters_set )

    helpers.simple_process_directory( sys.argv[ 1 ], sys.argv[ 2 ], noise, parameters )
    
    for param_set in parameters:
        param_set.file_postfix = "_[noise_colored]" + param_to_postfix( param_set )
    
    
    helpers.simple_process_directory( sys.argv[ 1 ], sys.argv[ 2 ], colored_noise, parameters )

    
    parameters = []
    
    probabilities = ( 0.001, 0.005, 0.01, 0.02, 0.04, 0.08, 0.15 )
    
    for probability in probabilities:
        parameters_set = helpers.Parameters()
        
        parameters_set.mean = 128
        parameters_set.stddev = 110
        parameters_set.probability = probability
        parameters_set.file_postfix = "_[noise_peak]_[probability=" + str( probability ) + "]" + param_to_postfix( parameters_set )
        
        parameters.append( parameters_set )
    
    helpers.simple_process_directory( sys.argv[ 1 ], sys.argv[ 2 ], burned_pixels, parameters )
    
if __name__ == "__main__":
    run()