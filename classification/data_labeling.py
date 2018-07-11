import numpy
import sys

import optical_comparision.should_accept as should_accept
import loading

## ======================= ##
##
def save_binary( data, file_path ):

    numpy.save( file_path, data )

## ======================= ##
##
def label_row( row ):
    
    label = should_accept.should_accept( row )
    if label == should_accept.ShouldAccept.TRUE:
        return "TRUE"
    elif label == should_accept.ShouldAccept.FALSE:
        return "FALSE"
    elif label == should_accept.ShouldAccept.IGNORE:
        return "IGNORE"
    else:
        return "DONT_KNOW"
    
    
## ======================= ##
##
def label_data( src_file, dest_file ):

    data = loading.load_dataset( src_file )

    # for i in range(1,100):
    #     print( data[i]["psnr"] )

    print( "Creating new array" )
    new_dtype = numpy.dtype( [('scene', 'S17')] + data.dtype.descr + [('label', 'S9')] )
    labeled_data = numpy.zeros( data.shape, dtype=new_dtype )
    
    print( "Coping content to new array" )
    for name in data.dtype.names:
        labeled_data[ name ] = data[ name ]

    print("Sceneing data")
    scene_names = [ should_accept.get_scene_name(row["image"].decode('UTF-8')) for row in data ]
    labeled_data["scene"] = scene_names

    print( "Labeling data" )
    labels = [ label_row( row ) for row in data ]
    labeled_data[ "label" ] = labels

    print( "Saving file [" + dest_file + "]" )
    save_binary( labeled_data, dest_file )
    
    
## ======================= ##
##
def run():

    print( "psnred: " + str( should_accept.get_psnred() ) )
    label_data( sys.argv[ 1 ], sys.argv[ 2 ] )
    print( "psnred: " + str( should_accept.get_psnred() ) )

    

if __name__ == "__main__":
    run()
    