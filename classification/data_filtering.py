import numpy
import sys
import pandas
import optical_comparision.should_accept as should_accept
import loading

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
def save_binary( data, file_path ):

    print( "Saving file [" + file_path + "]" )
    numpy.save( file_path, data )
    
## ======================= ##
##
def convert_to_binary( src_file, target_file, scenes_to_remove = [] ):

    print( "Loading file [" + src_file + "]" )
    data = loading.load_dataset( src_file )
    # data = numpy.recfromcsv( src_file, delimiter=',', names=True )

    filtered = [ row for row in data if not should_accept.get_scene_name( row[ "image" ].decode('UTF-8') ) in scenes_to_remove ]

    save_binary( filtered, target_file )
    
## ======================= ##
##
def remove_names_from_data( src_file, target_file ):

    data = numpy.recfromcsv( src_file, delimiter=',', names=True )
    data = remove_names( data )
    
    data.to_csv( target_file )
    
    
## ======================= ##
##
def run():

    #remove_names_from_data( sys.argv[ 1 ], sys.argv[ 2 ] )
    scenes_to_remove = sys.argv[ 3: ]
    convert_to_binary( sys.argv[ 1 ], sys.argv[ 2 ], scenes_to_remove )

    

if __name__ == "__main__":
    run()


