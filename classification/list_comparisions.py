import sys
import os



## ======================= ##
##
def is_valid_image_file( file_name ):
    return (file_name.endswith(".png") or file_name.endswith(".jpg")) \
           or file_name.endswith(".jpeg") or file_name.endswith(".exr") \
           and "output" not in file_name

## ======================= ##
##
def list_files( directory ):

    for ( dirpath, dirnames, filenames ) in os.walk( directory ):
        return filenames

## ======================= ##
##
def list_directories( directory ):
    
    return next(os.walk(directory))[ 1 ]
        
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
def make_relative( relative, path ):
    return os.path.join( relative, path )

        
## ======================= ##
##
def make_relative_path( pair, relative_dir ):
    return ( make_relative( relative_dir, pair[ 0 ] ), make_relative( relative_dir, pair[ 1 ] ) )
        
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
        print( "    Looking for reference images in [" + reference_path + "]")
        
        reference_files = list_files( reference_path )
        
        if reference_files is None or files is None:
            continue
        
        # get rid of non-image files.
        reference_files = [ file for file in reference_files if is_valid_image_file( file ) ]
        files = [ file for file in files if is_valid_image_file( file ) ]
        
        pairs = pair_image_with_reference( files, reference_files )
        pairs = [ make_relative_path( pair, relative_directory ) for pair in pairs ]
        
        comparision_list.extend( pairs )
        
        print( "    Found " + str( len( pairs ) ) + " pairs of files to compare." )
        
    return comparision_list
        

## ======================= ##
##
def all_combinations( files ):
    
    combintations = []
    
    for first in range( 0, len( files ) ):
        for second in range( 0, first ):
            combintations.append( ( files[ first ], files[ second ] ) )
    
    return combintations


## ======================= ##
##
def match_diff_seeds( files1, files2 ):

    matches = []
    
    for file in files1:
        if file in files2:
            matches.append( file )
            
    return matches
    
## ======================= ##
##
def list_different_seeds( directory1, directory2 ):

    # consists of pairs of files to compare
    comparision_list = []

    for root, dirs, files in os.walk( directory1 ):
    
        relative_directory1 = os.path.relpath( root, directory1 )
        reference_path = os.path.join( directory2, relative_directory1 )
        
        print( "Processing directory: [" + root + "]" )
        print( "    Looking for reference images in [" + reference_path + "]")
        
        reference_files = list_files( reference_path )
        
        if reference_files is None or files is None:
            continue

        # get rid of non-image files.
        reference_files = [ file for file in reference_files if is_valid_image_file( file ) ]
        files = [ file for file in files if is_valid_image_file( file ) ]
        
        matches = match_diff_seeds( files, reference_files )
        pairs = [ ( os.path.join( root, match ), os.path.join( reference_path, match ) ) for match in matches ]
                
        comparision_list.extend( pairs )
        
        print( "    Found " + str( len( pairs ) ) + " pairs of files to compare." )
    
    return comparision_list     
                
    
## ======================= ##
##
def list_all_combinations_comparisions( directory ):
       
    # consists of pairs of files to compare
    comparision_list = []
    
    for root, dirs, files in os.walk( directory ):
    
        relative_directory = os.path.relpath( root, directory )
        
        print( "Processing directory: [" + root + "]" )    
        
        # get rid of non-image files.
        files = [ file for file in files if is_valid_image_file( file ) ]
        
        pairs = all_combinations( files )
        pairs = [ make_relative_path( pair, relative_directory ) for pair in pairs ]
        
        comparision_list.extend( pairs )
        
        print( "    Found " + str( len( pairs ) ) + " pairs of files to compare." )
    
    return comparision_list
        
        
## ======================= ##
##
def list_all_in_subdirs( reference_dir, compare_dir_parent, subdirs ):
    
    comparision_list = []
    
    print( "Processing subdirectories: " + str( subdirs ) + "\n")
    
    for subdir in subdirs:
    
        dir = make_relative( compare_dir_parent, subdir )
    
        list = list_reference_comparisions( dir, reference_dir )
        pairs = [ ( make_relative( reference_dir, pair[ 0 ] ), make_relative( dir, pair[ 1 ] ) ) for pair in list ]
        
        comparision_list.extend( pairs )
        
        
    print( "Processing combinations with different sampling rate in subdirectory: " + str( reference_dir ) + "\n")
    
    pairs = list_all_combinations_comparisions( reference_dir )
    pairs = [ ( make_relative( reference_dir, pair[ 0 ] ), make_relative( reference_dir, pair[ 1 ] ) ) for pair in pairs ]
    
    comparision_list.extend( pairs )

    return comparision_list
        
## ======================= ##
##
def list_all( reference_dir, compare_dir_parent ):

    subdirs = list_directories( compare_dir_parent )
    return list_all_in_subdirs( reference_dir, compare_dir_parent, subdirs )
    
    
        
## ======================= ##
##
def run():

    reference_dir = sys.argv[ 1 ]
    compare_dir_parent = sys.argv[ 2 ]

    #print( list_reference_comparisions( sys.argv[ 2 ], sys.argv[ 1 ] ) )
    #list = list_reference_comparisions( sys.argv[ 2 ], sys.argv[ 1 ] )
    #list = list_all( reference_dir, compare_dir_parent )
    list = list_different_seeds( reference_dir, compare_dir_parent )
    
    file = open("list.txt","w") 
    file.write( str( list ) )

        
        
if __name__ == "__main__":
    run()
