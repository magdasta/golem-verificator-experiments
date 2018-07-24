import loading
import numpy
import sys
import os


## ======================= ##
##
def change_paths( data ):

    for row in data:
        
        name1 = row[ "reference_image" ].decode('UTF-8')
        name2 = row[ "image" ].decode('UTF-8')
        
        name1 = name1.replace( "/home/imapp/Dokumenty/images_database_copy", "D:/GolemData/images_database" )
        name2 = name2.replace( "/home/imapp/Dokumenty/images_database_copy", "D:/GolemData/images_database" )
        
        name1 = os.path.normpath( name1 )
        name2 = os.path.normpath( name2 )
        
        row[ "reference_image" ] = name1
        row[ "image" ] = name2


## ======================= ##
##
def run():

    data = loading.load_dataset( sys.argv[ 1 ] )
    change_paths( data )
    loading.save_binary( data, sys.argv[ 2 ] )
    

if __name__ == "__main__":
    run()
    