from PIL import Image, ImageFilter
import sys
import os
import helpers




## ======================= ##
##
def blur( image, parameters ):

    return image.filter( ImageFilter.GaussianBlur( parameters.kernel_size ) )
    
      
## ======================= ##
##
def run():

    parameters = []

    for kernel_size in range( 1, 5 ):
        
        parameters_set = helpers.Parameters()
        parameters_set.kernel_size = kernel_size
        parameters_set.file_postfix = "_[blured]_" + "[kernel=" + str( kernel_size ) + "]"
        
        parameters.append( parameters_set )

    helpers.simple_process_directory( sys.argv[ 1 ], sys.argv[ 2 ], blur, parameters )

    
    
if __name__ == "__main__":
    run()
    
