import loading
import numpy


## ======================= ##
##
def merge_datasets( data1, data2 ):

    return numpy.append( data1, data2, dtype = data1.dtype )


## ======================= ##
##
def run():

    data = loading.load_dataset( sys.argv[ 1 ] )
    data2 = loading.load_dataset( sys.argv[ 2 ] )
    
    data = merge_datasets( data, data2 )
    
    loading.save_binary( sys.argv[ 3 ] )
    

if __name__ == "__main__":
    run()
    