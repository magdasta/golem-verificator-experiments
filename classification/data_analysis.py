import numpy
import matplotlib.pyplot
import sys
import os
import PIL
import pandas

import loading
import extract_features
import optical_comparision.should_accept as should_accept


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
def load_dataset( file_path ):

    print( "Loading file [" + file_path + "]" )
    
    ( file, ext ) = os.path.splitext( file_path )
    
    if ext == ".csv":
        return numpy.recfromcsv( file_path, delimiter=',', names=True )
    elif ext == ".npy":
        return numpy.load( file_path )
    else:
        return None

    
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
        return file + "[crop_x=" + str( row[ "crop_x" ] ) + "][crop_y=" + str( row[ "crop_y" ] ) + "][psnr_diff=" + str( row[ "psnr" ] ) + "]" + extension
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
def save_filtered_csv( dataset, file_path ):

    print( "Saving data to csv file [" + file_path + "]" )
    
    pandas_data = pandas.DataFrame( dataset )
    pandas_data.to_csv( file_path )
    
    
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
    data = loading.load_dataset( data_file )
    
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
def filter_correct( data ):

    samples_treshold = 2000

    print("Filtering image comparisions with different number of samples.")
    correct_images = data[data["samples"] != data["samples_reference"]]

    print("Filtering compared images with number of samples less then " + str(samples_treshold))
    correct_images = correct_images[correct_images["samples"] > samples_treshold]

    print("Filtering reference images with number of samples less then " + str(samples_treshold))
    correct_images = correct_images[correct_images["samples_reference"] > samples_treshold]

    return correct_images

## ======================= ##
##
def load_correct_images( csv_file ):

    data_file = csv_file
    data = load_dataset( data_file )

    correct_images = filter_correct( data )
    
    return correct_images
    
    
## ======================= ##
##
def filter_accepted_images( data ):

    print( "Choosing samples labeled as TRUE." )
    correct_images = data[ data[ "label" ] == b'TRUE' ] 
    
    return correct_images
    
## ======================= ##
##
def filter_damaged_images( data ):

    print( "Choosing samples labeled as FALSE." )
    damaged_images = data[ data[ "label" ] == b'FALSE' ] 
    
    return damaged_images
    
    
## ======================= ##
##
def load_accepted_images( data_file ):

    data = loading.load_dataset( data_file )
    return filter_accepted_images( data )
    
    
## ======================= ##
##
def load_damaged_images( data_file ):
    
    data = loading.load_dataset( data_file )
    return filter_damaged_images( data )
    
## ======================= ##
##
def load_damaged_accepted_set( data_file ):

    data = loading.load_dataset( data_file )
    
    damaged = filter_damaged_images( data )
    accepted = filter_accepted_images( data )
    
    return ( damaged, accepted )


## ======================= ##
##
def analyze_wavelets( data ):
    mask = [ should_accept.get_scene_name( row[ "image" ].decode( 'UTF-8' ) ) == "glass_material" for row in data]
    filtered = data[ mask ]
    filtered = filtered[ filtered[ "is_cropped" ] == True ]
    filtered = filtered[ filtered[ "crop_x" ] >= 1 ]
    filtered = filtered[ filtered[ "crop_x" ] <= 1 ]
    filtered = filtered[ filtered[ "crop_y" ] >= 4 ]
    filtered = filtered[ filtered[ "crop_y" ] <= 4 ]
    
    filtered = filtered[ filtered["samples"] != filtered["samples_reference"] ]
    filtered = filtered[ filtered["samples_reference"] == 8325 ]
    
    plot_data( "samples", "wavelet_high", filtered )
    plot_data( "samples", "wavelet_low", filtered )
    plot_data( "samples", "wavelet_mid", filtered )
    
    matplotlib.pyplot.show()

def save_all_crops( data, compared_dir, reference_dir ):
    data = data[ data[ "is_cropped" ] == True ]

    num_crops = 10

    for scene in should_accept.ok_thresholds:
        filtered = data[ data[ "samples" ] == should_accept.ok_thresholds[ scene ] ]
        filtered = filtered[ filtered[ "samples_reference" ] == should_accept.not_ok_thresholds[ scene ] ]
        for row in filtered:
            if should_accept.get_scene_name( row[ "image" ].decode( 'UTF-8' ) ):
                reference_file = os.path.normpath(row["reference_image"].decode('UTF-8'))
                compared_file = os.path.normpath(row["image"].decode('UTF-8'))

                print("Processing files: reference [" + reference_file + "] and compared [" + compared_file + "].")

                (reference_image, compared_image) = load_images(reference_file, compared_file)

                (cropped_image, cropped_reference) = extract_features.crop_image(row["crop_x"], row["crop_y"], num_crops, compared_image, reference_image)

                cropped_image.save(os.path.join(compared_dir, gen_file_name(compared_file, row)), "PNG")
                cropped_reference.save(os.path.join(reference_dir, gen_file_name(reference_file, row)), "PNG")


## ======================= ##
##
def run():

    data = loading.load_dataset( sys.argv[ 1 ] )
    save_all_crops( data, sys.argv[ 2 ], sys.argv[ 3 ] )


    # analyze_wavelets( data )

    # #save_filtered_dataset( load_datasets( sys.argv[ 1 ] )[ 0 ], sys.argv[ 2 ], sys.argv[ 3 ] )
    # #show_cropped_plot( "ref_edge_factor", "ssim" )
    
    # ( damaged, correct ) = load_damaged_accepted_set( sys.argv[ 1 ] )
    
    # correct = correct[ correct[ "ref_edge_factor" ] > 25 ]
    # correct = correct[ correct[ "ssim" ] < 0.92 ]
    
    # #damaged = damaged[ damaged[ "ref_edge_factor" ] > 25 ]
    
    
    # #print( correct[ "ref_edge_factor" ] )
    # save_filtered_dataset( correct, sys.argv[ 2 ], sys.argv[ 3 ] )
    # #save_filtered_csv( correct, sys.argv[ 2 ] )
    
    # plot_single_set( "ref_edge_factor", "ssim", correct )
    

if __name__ == "__main__":
    run()

    
    