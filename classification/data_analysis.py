import numpy
import matplotlib.pyplot
import sys
import os
import PIL


import extract_features


## ======================= ##
##
def create_directory_if_doesnt_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)

## ======================= ##
##
def load_images( reference_file, compared_file ):

    ref_image = PIL.Image.open( reference_file )
    compared_image = PIL.Image.open( compared_file )
    
    return ( ref_image, compared_image )

    
## ======================= ##
##
def flatten_path( path ):

    drive, path_and_file = os.path.splitdrive( os.path.normpath( path ) )
    splitted = path_and_file.split( os.sep )

    splitted.pop( 0 )
    
    flattened = splitted[ 0 ]
    splitted.pop( 0 )
    
    for component in splitted:
        flattened = flattened + "_" + component
        
    return flattened

## ======================= ##
##
def gen_file_name( file_path, row ):
    
    flattened = flatten_path( file_path )
    
    if row[ "is_cropped" ]:
        ( file, extension ) = os.path.splitext( flattened )
        return file + "[crop_x=" + str( row[ "crop_x" ] ) + "][crop_y=" + str( row[ "crop_y" ] ) + "]" + extension
    else:
        return flattened
    
    
## ======================= ##
##
def save_filtered_dataset( dataset, reference_dir, compared_dir ):
    
    print( "\n## ===================================================== ##" )
    print( "Saving filtered dataset." )
    
    create_directory_if_doesnt_exist( reference_dir )
    create_directory_if_doesnt_exist( compared_dir )
    
    reference_file = ""
    compared_file = ""
    
    reference_image = None
    compared_image = None
    
    num_crops = 10
    
    for index in range( 0, dataset.shape[ 0 ] ):
        
        row = dataset[ index ]
        
        # If processed image file changed, load new image.
        if row[ "reference_image" ] != reference_file or row[ "image" ] != compared_file:
            
            reference_file = os.path.normpath( row[ "reference_image" ].decode('UTF-8') )
            compared_file = os.path.normpath( row[ "image" ].decode('UTF-8') )
            
            print( "Processing files: reference [" + reference_file + "] and compared [" + compared_file + "]." )
            
            ( reference_image, compared_image ) = load_images( reference_file, compared_file )
            
        if row[ "is_cropped" ]:
        
            ( cropped_image, cropped_reference ) = extract_features.crop_image( row[ "crop_x" ], row[ "crop_y" ], num_crops, compared_image, reference_image )
            
            cropped_image.save( os.path.join( compared_dir, gen_file_name( compared_file, row ) ), "PNG" )
            cropped_reference.save( os.path.join( reference_dir, gen_file_name( reference_file, row ) ), "PNG" )
            
        else:
            
            compared_image.save( os.path.join( compared_dir, gen_file_name( compared_file, row ) ), "PNG" )
            reference_image.save( os.path.join( reference_dir, gen_file_name( reference_file, row ) ), "PNG" )
        
    
    
## ======================= ##
##
def plot_data( xlabel, ylabel, data ):
    
    matplotlib.pyplot.scatter( data[ xlabel ], data[ ylabel ] )

    matplotlib.pyplot.xlabel( xlabel )
    matplotlib.pyplot.ylabel( ylabel )

    
## ======================= ##
##
def show_multidata( xlabel, ylabel, data_list ):
    
    for data in data_list:
        plot_data( xlabel, ylabel, data )
        
    matplotlib.pyplot.show()

## ======================= ##
##
def plot_single_set( xlabel, ylabel, data ):
    
    plot_data( xlabel, ylabel, data )
    matplotlib.pyplot.show()
    
    
## ======================= ##
##
def load_datasets( csv_file ):

    data_file = csv_file
    data = numpy.recfromcsv( data_file, delimiter=',', names=True )

    #data = data[ data[ "ref_edge_factor" ] > 20 ]
    
    damage = data[ data[ "samples" ] == data[ "samples_reference" ] ]
    diffrent_sampling = data[ data[ "samples" ] != data[ "samples_reference" ] ] 
    
    return ( damage, diffrent_sampling )
    

## ======================= ##
##
def show_cropped_plot( xlabel, ylabel ):
    
    damage, diffrent_sampling = load_datasets( sys.argv[ 1 ] )
    
    damage = damage[ damage[ "is_cropped" ] == True ]
    diffrent_sampling = diffrent_sampling[ diffrent_sampling[ "is_cropped" ] == True ]
    
    diffrent_sampling = diffrent_sampling[ diffrent_sampling[ "samples" ] > 2000 ]
    diffrent_sampling = diffrent_sampling[ diffrent_sampling[ "samples_reference" ] > 2000 ]
    
    #show_multidata( xlabel, ylabel, ( diffrent_sampling, damage ) )
    #show_multidata( xlabel, ylabel, ( damage ) )

    plot_data( xlabel, ylabel, diffrent_sampling )
    matplotlib.pyplot.show()
    
## ======================= ##
##
def load_correct_images( csv_file ):
    
    print( "Loading file [" + csv_file + "]" )
    
    samples_treshold = 2000
    
    data_file = csv_file
    data = numpy.recfromcsv( data_file, delimiter=',', names=True )
    
    print( "Filtering image comparisions with different number of samples." )
    correct_images = data[ data[ "samples" ] != data[ "samples_reference" ] ] 
    
    print( "Filtering compared images with number of samples less then " + str( samples_treshold ) )
    correct_images = correct_images[ correct_images[ "samples" ] > samples_treshold ]
    
    print( "Filtering reference images with number of samples less then " + str( samples_treshold ) )
    correct_images = correct_images[ correct_images[ "samples_reference" ] > samples_treshold ]
    
    return correct_images
    
## ======================= ##
##
def run():

    #save_filtered_dataset( load_datasets( sys.argv[ 1 ] )[ 0 ], sys.argv[ 2 ], sys.argv[ 3 ] )
    #show_cropped_plot( "ref_edge_factor", "ssim" )
    
    correct = load_correct_images( sys.argv[ 1 ] )
    #correct = correct[ correct[ "ssim" ] < 0.91 ]
    
    #save_filtered_dataset( correct, sys.argv[ 2 ], sys.argv[ 3 ] )
    
    
    plot_single_set( "ref_edge_factor", "ssim", correct )
    

if __name__ == "__main__":
    run()

    
    