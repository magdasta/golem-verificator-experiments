import numpy



class ThresholdSSIM:

    def __init__( self, threshold ):
        self.ssim_threshold = threshold

        
    ## ======================= ##
    ##
    def compute_label( self, row ):
        
        if row[ "ssim" ] >= self.ssim_threshold:
            return b"TRUE"
        else:
            return b"FALSE"
        
    ## ======================= ##
    ##
    def classify( self, data_set ):
        
        return numpy.array( [ self.compute_label( row ) for row in data_set ] )
    
