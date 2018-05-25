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
def smooth_image( src_file, target_file ):

    image = Image.open( src_file )
    smoothed = smooth( image, None )
    smoothed.save( target_file )
      
## ======================= ##
##
def smooth_images( src_file, target_dir ):
    
    [ file_name, extension ] = os.path.splitext( os.path.basename( src_file ) ) 
    target_file = file_name + "_smoothed" + extension
    target_path = os.path.join( target_dir, target_file )
    
    smooth_image( src_file, target_path )
      
## ======================= ##
##
def run():

    helpers.process_directory( sys.argv[ 1 ], sys.argv[ 2 ], smooth_images )

    
    
if __name__ == "__main__":
    run()
    
