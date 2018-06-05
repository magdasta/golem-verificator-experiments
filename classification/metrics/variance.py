from PIL import Image
import numpy


## ======================= ##
##
class ImageVariance:
    

    ## ======================= ##
    ##
    def compute_metrics( this, image1, image2 ):

        image1 = image1.convert("RGB")
        image2 = image2.convert("RGB")
        
        np_image1 = numpy.array( image1 )
        np_image2 = numpy.array( image2 )
        
        reference_variance = numpy.var( np_image1, axis=( 0, 1 ) )
        image_variance = numpy.var( np_image2, axis=( 0, 1 ) )
        
        reference_variance = reference_variance[ 0 ] + reference_variance[ 1 ] + reference_variance[ 2 ]
        image_variance = image_variance[ 0 ] + image_variance[ 1 ] + image_variance[ 2 ]
        
        result = dict()
        result[ "reference_variance" ] = reference_variance
        result[ "image_variance" ] = image_variance
        result[ "variance_diff" ] = reference_variance - image_variance
        
        return result
    
    ## ======================= ##
    ##
    def get_labels( this ):
        return [ "reference_variance", "image_variance", "variance_diff" ]
        
        