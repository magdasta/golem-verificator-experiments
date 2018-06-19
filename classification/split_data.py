import numpy
import sys
import os

import loading


## ======================= ##
##
def split_set( data, proportion ):

    data_size = data.shape[ 0 ]
    
    random = numpy.random.rand( data_size )
    train_mask = random[:] < proportion
    test_mask = random[:] >= proportion
    
    train_set = data[ train_mask ]
    test_set = data[ test_mask ]
    
    return train_set, test_set
    

## ======================= ##
##
def split_train_test_set( data_file, output_dir, proportion ):

    data = loading.load_dataset( data_file )

    train_set, test_set = split_set( data, proportion )
    
    basename = os.path.basename( data_file )
    (name, ext) = os.path.splitext( basename )
    
    test_name = os.path.join( output_dir, name + "_test" + ext )
    train_name = os.path.join( output_dir, name + "_train" + ext )
    
    loading.save_binary( train_set, train_name )
    loading.save_binary( test_set, test_name )


## ======================= ##
##
def run():

    split_train_test_set( sys.argv[ 1 ], sys.argv[ 2 ], 0.7 )
    
    

if __name__ == "__main__":
    run()