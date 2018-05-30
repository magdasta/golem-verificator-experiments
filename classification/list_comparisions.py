import sys
import os


## ======================= ##
##
def list_files( directory ):

    for ( dirpath, dirnames, filenames ) in os.walk( directory ):
        return filenames

        
        
## ======================= ##
##
def match_single_reference_file( reference_file, images ):

    # Reference file name should have common part with some elements from images list.
    reference_file = os.path.splitext( reference_file )[ 0 ]
    return [image_name for image_name in images if reference_file in image_name]

        
## ======================= ##
##
def pair_image_with_reference( images, reference_files ):

    comparision_pairs = []

    # Single reference image can be compared to multiple images.
    for reference in reference_files:
        
        match_list = match_single_reference_file( reference, images )
        
        for match in match_list:
            comparision_pairs.append( ( reference, match ) )
            
    return comparision_pairs
        

## ======================= ##
##
def list_reference_comparisions( images_dir, reference_dir ):

    # consists of pairs of files to compare
    comparision_list = []
    
    # List files in images_dir (and subdirectories), find image to compare in reference_dir.
    # Directories structures in both images_dir and reference_dir should look the same way.
    for root, dirs, files in os.walk( images_dir ):
    
        relative_directory = os.path.relpath( root, images_dir )
        reference_path = os.path.join( reference_dir, relative_directory )
        
        print( "Processing directory: [" + root + "]" )
        print( "Looking for reference images in [" + reference_path + "]")
        
        reference_files = list_files( reference_path )
        
        pairs = pair_image_with_reference( files, reference_files )
        comparision_list.extend( pairs )
        
    return comparision_list
        

## ======================= ##
##
def run():

    print( list_reference_comparisions( sys.argv[ 2 ], sys.argv[ 1 ] ) )
    #list_reference_comparisions( sys.argv[ 2 ], sys.argv[ 1 ] )
        
if __name__ == "__main__":
    run()
