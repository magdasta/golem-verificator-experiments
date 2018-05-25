from PIL import Image, ImageFilter
import sys

## ======================= ##
##
def smooth( image, parameters ):

    return image.filter( ImageFilter.SMOOTH )
    
## ======================= ##
##
def smooth_image( src_file, target_file ):

    image = Image.open( src_file )
    smoothed = smooth( image, None )
    smoothed.save( target_file )
    
    
smooth_image( sys.argv[ 1 ], sys.argv[ 2 ] )