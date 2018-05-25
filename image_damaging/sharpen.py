from PIL import Image, ImageFilter
import sys
import os
import helpers


## ======================= ##
##
def sharpen( image, parameters ):

    return image.filter( ImageFilter.SHARPEN )
    

## ======================= ##
##
def run():

    parameters = []
    parameters_set = helpers.Parameters()
    parameters_set.file_postfix = "_sharpened"
    
    parameters.append( parameters_set )

    helpers.simple_process_directory( sys.argv[1], sys.argv[2], sharpen, parameters )
    
## ======================= ##
##
if __name__ == "__main__":
    run()
    
    