import numpy
from skimage.measure import compare_ssim as compare_ssim

import sys


## ======================= ##
##
class MetricSSIM:
    

    ## ======================= ##
    ##
    def compute_metrics( this, image1, image2 ):

        image1 = image1.convert("RGB")
        image2 = image2.convert("RGB")
        
        np_image1 = numpy.array( image1 )
        np_image2 = numpy.array( image2 )
        
        structualSim = compare_ssim( np_image1, np_image2, multichannel=True )
        
        result = dict()
        result[ "ssim" ] = structualSim
        
        return result
    
    ## ======================= ##
    ##
    def get_labels( this ):
        return [ "ssim" ]
    
## ======================= ##
##
def run():

    first_img = sys.argv[ 1 ]
    second_img = sys.argv[ 2 ]
    
    ssim = MetricSSIM()
    
    print( ssim.compute_metrics( first_img, second_img ) )
    
    
    
if __name__ == "__main__":
    run()
    