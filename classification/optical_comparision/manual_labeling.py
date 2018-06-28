import cv2
import numpy

import sys




## ======================= ##
##
def main_loop( image_path ):

    image = cv2.imread( image_path, cv2.IMREAD_COLOR )
    screen = numpy.zeros( (512,512,4), numpy.uint8 )
    
    cv2.namedWindow( 'Crops labeling' )
    
    while(1):
    
        cv2.imshow( 'Crops labeling', image )
        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()


## ======================= ##
##
def run():

    main_loop( sys.argv[ 1 ] )

        
        
if __name__ == "__main__":
    run()



