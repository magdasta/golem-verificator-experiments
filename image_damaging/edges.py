from PIL import ImageFilter
import sys
import helpers


## ======================= ##
##
def find_edges( image, parameters ):

    return image.filter( ImageFilter.FIND_EDGES )
    

## ======================= ##
##
def run():

    parameters = []
    parameters_set = helpers.Parameters()
    parameters_set.file_postfix = "_[edged]"
    
    parameters.append( parameters_set )

    helpers.simple_process_directory( sys.argv[1], sys.argv[2], find_edges, parameters )
    
## ======================= ##
##
if __name__ == "__main__":
    run()
    
    