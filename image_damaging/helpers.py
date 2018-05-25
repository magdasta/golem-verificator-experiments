import sys
import os
from PIL import Image


## ======================= ##
##
class Parameters:
    pass


## ======================= ##
##
def create_directory_if_doesnt_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)

## ======================= ##
##
def is_valid_image_file( file_name ):
    return (file_name.endswith(".png") or file_name.endswith(".jpg")) \
           or file_name.endswith(".jpeg") or file_name.endswith(".exr") \
           and "output" not in file_name

## ======================= ##
##
def process_image( src_file, target_file, processor, parameters ):
    
    image = Image.open( src_file )
    processed = processor( image, parameters )
    processed.save( target_file )
        
        
## ======================= ##
##
def process_directory( src_dir, target_dir, processor ):

    source_images_directory = src_dir
    create_directory_if_doesnt_exist( target_dir )
    
    for root, dirs, files in os.walk( source_images_directory ):
    
        subdirectory_name = os.path.relpath( root, source_images_directory )
        results_directory = os.path.join( target_dir, subdirectory_name )
        create_directory_if_doesnt_exist( results_directory )
    
        print ( "\n" )
        print( "## =========================================================== ##" )
        print( "Processing files in directory: [" + root + "]. Target directory: [" +  results_directory + "]:\n" )
    
        for file_name in files:
        
            src_path = os.path.join( root, file_name )        
            if is_valid_image_file( file_name ):
                
                print( "Processing file: [" + src_path + "]."  )
                
                processor( src_path, results_directory )
                
            else:
                print( "Ignoring file: [" + src_path + "] as not valid image." )
                
                
    
    

