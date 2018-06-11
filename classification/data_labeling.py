import numpy
import sys
import os
import pandas

import optical_comparision.should_accept as labels
import loading


## ======================= ##
##
def save_binary( data, file_path ):

    numpy.save( file_path, data )

## ======================= ##
##
def label_row( row ):
    
    reference_path = row[ "reference_image" ].decode( 'UTF-8' )
    compared_path = row[ "image" ].decode( 'UTF-8' )
    
    label = labels.should_accept( reference_path, compared_path )
    if label == labels.ShouldAccept.TRUE:
        return "TRUE"
    elif label == labels.ShouldAccept.FALSE:
        return "FALSE"
    else:
        return "DONT_KNOW"
    
    
## ======================= ##
##
def label_data( src_file, dest_file ):

    data = loading.load_dataset( src_file )
    
    print( "Creating new array" )
    new_dtype = numpy.dtype( data.dtype.descr + [('label', 'S9')] )
    labeled_data = numpy.zeros( data.shape, dtype=new_dtype )
    
    print( "Coping content to new array" )
    for name in data.dtype.names:
        labeled_data[ name ] = data[ name ]
    
    print( "Labeling data" )
    labels = [ label_row( row ) for row in data ]
    labeled_data[ "label" ] = labels
    
    print( "Saving file [" + dest_file + "]" )
    save_binary( labeled_data, dest_file )
    
    
## ======================= ##
##
def run():

    label_data( sys.argv[ 1 ], sys.argv[ 2 ] )
    
    

if __name__ == "__main__":
    run()
    