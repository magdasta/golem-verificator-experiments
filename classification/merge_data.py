import loading
import numpy
import sys
import numpy.lib.recfunctions as rfn


## ======================= ##
##
def merge_datasets( data1, data2 ):

    # return rfn.merge_arrays(( data1, data2 ), flatten=True, usemask=False)

    # return numpy.append( data1, data2 )

    masked = rfn.stack_arrays( [data1, data2], autoconvert=True )

    data = numpy.zeros(masked.shape, dtype=masked.dtype)

    for name in masked.dtype.names:
        data[ name ] = masked[ name ]

    return data

    # print( rfn.zip_descr( [data1, data2], flatten = True ) )


## ======================= ##
##
def print_dtype_descr( type_desc ):

    for column in type_desc:
        print( column[ 1 ] + "      " + column[ 0 ] )
   
## ======================= ##
##
def print_dtype( data ):
    print_dtype_descr( data.dtype.descr )
   
## ======================= ##
##
def is_label_in( label, type ):

    for column in type.descr:
        if column[ 0 ] == label[ 0 ]:
            return True
    return False
    
## ======================= ##
##
def compute_additional_labels( type1, type2 ):
    
    additional_labels = list()
    
    for column in type2.descr:
        if not is_label_in( column, type1 ):
            additional_labels.append( column )
    
    return additional_labels

## ======================= ##
##
def build_index_mapping( data1, data2 ):

    

    
## ======================= ##
##
def merge_datasets_new_metrics( data1, data2 ):
    
    print( "Computing dataset columns." )
    additional_labels = compute_additional_labels( data1.dtype, data2.dtype )
    
    print( "Additional columns to add to dataset:" )
    print_dtype_descr( additional_labels )
    print( "" )
    
    print( "Creating new array" )
    new_dtype = numpy.dtype( data1.dtype.descr + additional_labels )
    extended_dataset = numpy.zeros( data1.shape, dtype=new_dtype )
    
    print( "Coping content to new array" )
    for name in data1.dtype.names:
        extended_dataset[ name ] = data1[ name ]
        

    
    return None
    
    
## ======================= ##
##
def run():

    data = loading.load_dataset( sys.argv[ 1 ] )
    print_dtype( data )
    
    data2 = loading.load_dataset( sys.argv[ 2 ] )
    print_dtype( data2 )

    #data = merge_datasets( data, data2 )
    #print( data.dtype )
    
    merge_datasets_new_metrics( data, data2 )
    
    #loading.save_binary( data, sys.argv[ 3 ] )
    

if __name__ == "__main__":
    run()
    