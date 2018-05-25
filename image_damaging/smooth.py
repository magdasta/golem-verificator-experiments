from PIL import Image, ImageFilter
import sys
import os
import helpers




## ======================= ##
##
def smooth( image, parameters ):

    return image.filter( ImageFilter.SMOOTH )
    
      
## ======================= ##
##
def run():

    parameters = []
    parameters_set = helpers.Parameters()
    parameters_set.file_postfix = "_smoothed"
    
    parameters.append( parameters_set )

    helpers.simple_process_directory( sys.argv[ 1 ], sys.argv[ 2 ], smooth, parameters )

    
    
if __name__ == "__main__":
    run()
    
