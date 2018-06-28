from PIL import Image, ImageMath
import sys
import helpers
import math


## ======================= ##
##
def add_images( image, add_r, add_g, add_b ):

    channels = image.split()
    
    expression = "convert( a+b, 'L' )"
    
    added_r = ImageMath.eval( expression, a=channels[ 0 ], b=add_r )
    added_g = ImageMath.eval( expression, a=channels[ 1 ], b=add_g )
    added_b = ImageMath.eval( expression, a=channels[ 2 ], b=add_b )
    
    return Image.merge( 'RGB', ( added_r, added_g, added_b ) )

## ======================= ##
##
def add_watermark( image, parameters ):

    width = image.width
    height = image.height
    
    width_excess = parameters.watermark.width - width
    height_excess = parameters.watermark.height - height

    left = math.floor(width_excess / 2)
    top = math.floor(height_excess / 2)
    right = left + width
    bottom = top + height
    
    watermark = parameters.watermark.crop( ( left, top, right, bottom ) )
    watermark = watermark.point( lambda i: i * parameters.alpha )

    return add_images( image, watermark, watermark, watermark )
    
      
## ======================= ##
##
def run():

    parameters = []
    
    watermark = Image.open( sys.argv[ 3 ] )
    watermark = watermark.split()[ 0 ]      # one channel is enough as long image is whole white
    alphas = [ 0.01, 0.05, 0.1, 0.15, 0.25, 0.5 ]
    
    for alpha in alphas:
        parameters_set = helpers.Parameters()
        parameters_set.watermark = watermark
        parameters_set.alpha = alpha
        parameters_set.file_postfix = "_[watermark]_[alpha=" + str( alpha ) + "]"
        
        parameters.append( parameters_set )

    helpers.simple_process_directory( sys.argv[ 1 ], sys.argv[ 2 ], add_watermark, parameters )

    
    
if __name__ == "__main__":
    run()
    
