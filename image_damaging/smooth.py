from PIL import Image, ImageFilter
import sys
import os
import helpers




## ======================= ##
##
def smooth( image, parameters ):

    return image.filter( ImageFilter.SMOOTH )
    
      
## ======================= ##
##
def smooth_images( src_file, target_dir ):
    
    [ file_name, extension ] = os.path.splitext( os.path.basename( src_file ) ) 
    target_file = file_name + "_smoothed" + extension
    target_path = os.path.join( target_dir, target_file )
    
    helpers.process_image( src_file, target_path, smooth, None )
      
## ======================= ##
##
def run():

    helpers.process_directory( sys.argv[ 1 ], sys.argv[ 2 ], smooth_images )

    
    
if __name__ == "__main__":
    run()
    
