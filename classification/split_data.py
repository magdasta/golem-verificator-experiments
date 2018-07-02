import numpy
import sys
import os

import loading
import optical_comparision.should_accept as accept



## ======================= ##
##
test_set = { "metal", "mug", "toughship", "breakfast_room", "plushy", "glass_material" }


## ======================= ##
##
def split_by_scenes( data, scenes ):
    
    test_set = [ row for row in data if accept.get_scene_name( row[ "image" ].decode('UTF-8') ) in scenes ]
    train_set = [ row for row in data if accept.get_scene_name( row[ "image" ].decode('UTF-8') ) not in scenes ]
    
    return train_set, test_set
    

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
def split_train_test_set( data_file, output_dir, split_fun, params ):

    data = loading.load_dataset( data_file )

    train_set, test_set = split_fun( data, params )
    
    basename = os.path.basename( data_file )
    (name, ext) = os.path.splitext( basename )
    
    test_name = os.path.join( output_dir, name + "_test" + ext )
    train_name = os.path.join( output_dir, name + "_train" + ext )
    
    loading.save_binary( train_set, train_name )
    loading.save_binary( test_set, test_name )


## ======================= ##
##
def run():

    #split_train_test_set( sys.argv[ 1 ], sys.argv[ 2 ], split_set, 0.7 )
    split_train_test_set( sys.argv[ 1 ], sys.argv[ 2 ], split_by_scenes, test_set )
    
    

if __name__ == "__main__":
    run()