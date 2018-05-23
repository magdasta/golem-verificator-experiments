import itk
import os
from sys import argv


## ====================================
##
def _ensure_dir( file_path ):
    directory = os.path.dirname( file_path )
    if not os.path.exists( directory ):
        os.makedirs( directory )

## ====================================
##
def load_image( file_path ):

    return itk.imread( file_path )

## ====================================
##
def save_image( file_path, image ):

    itk.imwrite( image, file_path )
    


output = load_image( argv[ 1 ] )
save_image( argv[ 2 ], output )