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
def run():

    data = loading.load_dataset( sys.argv[ 1 ] )
    print( data.dtype )
    data2 = loading.load_dataset( sys.argv[ 2 ] )
    print( data2.dtype )

    data = merge_datasets( data, data2 )
    print( data.dtype )
    
    loading.save_binary( data, sys.argv[ 3 ] )
    

if __name__ == "__main__":
    run()
    