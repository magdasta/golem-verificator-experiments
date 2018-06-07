import numpy
import sys
import os
import pandas

import data_analysis



## ======================= ##
##
def columns_indicies( data, names_list ):
    
    indicies = []
    names = list( data.dtype.names )
    
    for name in names_list:
        
        index = names.index( name )
        indicies.append( index )
        
    return indicies


## ======================= ##
##
def remove_columns( data, columns_list ):

    pandas_data = pandas.DataFrame( data )
    return pandas_data.drop( columns_list, 1 )
    
    
## ======================= ##
##
def remove_names( data ):

    return remove_columns( data, [ "reference_image", "image" ] )
    

## ======================= ##
##
def run():

    data = numpy.recfromcsv( sys.argv[ 1 ], delimiter=',', names=True )
    data = remove_names( data )
    
    data.to_csv( sys.argv[ 2 ] )
    #numpy.savetxt( sys.argv[ 2 ], data )


if __name__ == "__main__":
    run()


