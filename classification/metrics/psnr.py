from PIL import Image
import numpy
from skimage.measure import compare_ssim as compare_ssim
from skimage.measure import compare_psnr as compare_psnr

import sys


## ======================= ##
##
class MetricPSNR:

    ## ======================= ##
    ##
    def compute_metrics( this, image1, image2 ):

        image1 = image1.convert("RGB")
        image2 = image2.convert("RGB")
        
        np_image1 = numpy.array( image1 )
        np_image2 = numpy.array( image2 )
        
        psnr = compare_psnr( np_image1, np_image2 )
        
        result = dict()
        result[ "psnr" ] = psnr
        
        return result
    
    ## ======================= ##
    ##
    def get_labels( this ):
        return [ "psnr" ]
    
## ======================= ##
##
def run():

    first_img = sys.argv[ 1 ]
    second_img = sys.argv[ 2 ]
    
    psnr = MetricPSNR()
    
    print( psnr.compute_metrics( first_img, second_img ) )
    
    
    
if __name__ == "__main__":
    run()

