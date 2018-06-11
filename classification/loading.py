import numpy
import os



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
        
        