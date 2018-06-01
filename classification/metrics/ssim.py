from PIL import Image
import numpy
from skimage.measure import compare_ssim as compare_ssim
from skimage.measure import compare_psnr as compare_psnr

import sys


## ======================= ##
##
class MetricSSIM:
    

    ## ======================= ##
    ##
    def compute_metrics( this, image_file1, image_file2 ):

        image1 = Image.open( image_file1 ).convert("RGB")
        image2 = Image.open( image_file2 ).convert("RGB")
        
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
    