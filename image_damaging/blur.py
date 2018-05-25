from PIL import Image, ImageFilter
import sys
import os
import helpers




## ======================= ##
##
def blur( image, parameters ):

    return image.filter( ImageFilter.GaussianBlur( parameters.kernel_size ) )
    
      
## ======================= ##
##
def blur_images( src_file, target_dir ):
    
    [ file_name, extension ] = os.path.splitext( os.path.basename( src_file ) ) 
    
    for blur_size in range( 1, 5 ):
        target_file = file_name + "_blured_" + str( blur_size ) + extension
        target_path = os.path.join( target_dir, target_file )
        
        print( "    Generating image: [" + target_path + "] blured with kernel_size: " + str( blur_size ) )
        
        parameters = helpers.Parameters()
        parameters.kernel_size = blur_size
        
        helpers.process_image( src_file, target_path, blur, parameters )
      
## ======================= ##
##
def run():

    parameters = []

    for kernel_size in range( 1, 5 ):
        
        parameters_set = helpers.Parameters()
        parameters_set.kernel_size = kernel_size
        parameters_set.file_postfix = "_blured_" + str( kernel_size )
        
        parameters.append( parameters_set )

    helpers.simple_process_directory( sys.argv[ 1 ], sys.argv[ 2 ], blur, parameters )

    
    
if __name__ == "__main__":
    run()
    
