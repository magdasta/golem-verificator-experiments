from PIL import Image, ImageFilter
import sys


## ======================= ##
##
def sharpen( image, parameters ):

    return image.filter( ImageFilter.SHARPEN )
    
## ======================= ##
##
def sharpen_image( src_file, target_file ):

    image = Image.open( src_file )
    sharpened = sharpen( image, None )
    sharpened.save( target_file )
    
    
sharpen_image( sys.argv[ 1 ], sys.argv[ 2 ] )