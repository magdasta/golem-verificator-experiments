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
def process_image( src_file, target_file, processor, parameters_set ):
    
    image = Image.open( src_file )
    processed = processor( image, parameters_set )
    processed.save( target_file )
        
## ======================= ##
##
def process_images( src_file, target_dir, processor, parameters ):
    
    [ file_name, extension ] = os.path.splitext( os.path.basename( src_file ) ) 
    
    for parameters_set in parameters:
    
        target_file = file_name + parameters_set.file_postfix + extension
        target_path = os.path.join( target_dir, target_file )
        
        print( "    Generating image: [" + target_path + "]" )
        
        process_image( src_file, target_path, processor, parameters_set )
        
## ======================= ##
## @param processors function which takes file to process and calls processing multiple times.
## @param parameters is list of parameters sets invoked for each image. This structure should contain
## file_postfix field which will be appended to src file name.
def process_directory( src_dir, target_dir, processor, parameters ):
    _process_directory( src_dir, target_dir, None, processor, parameters )

## ======================= ##
## @param processors function which takes PIL Image and generic parameters set.
## @param parameters is list of parameters sets invoked for each image. This structure should contain
## file_postfix field which will be appended to src file name.
def simple_process_directory( src_dir, target_dir, processor, parameters ):
    _process_directory( src_dir, target_dir, processor, None, parameters )            
                
## ======================= ##
## @param processors function which takes PIL Image and generic parameters set. Use only one processors or multi_processor
## @param multi_processor replaces process_images function. multi_processor should implement splitting parameters sets into calls
## @param parameters is list of parameters sets invoked for each image. This structure should contain
## file_postfix field which will be appended to src file name.
def _process_directory( src_dir, target_dir, processor, multi_processor, parameters ):

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
                
                if multi_processor:
                    multi_processor( src_path, results_directory, parameters )
                else:
                    process_images( src_path, results_directory, processor, parameters )
                
            else:
                print( "Ignoring file: [" + src_path + "] as not valid image." )
    
    

