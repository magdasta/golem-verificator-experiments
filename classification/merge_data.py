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
def print_dtype_descr( type_desc ):

    for column in type_desc:
        print( column[ 1 ] + "      " + column[ 0 ] )
   
## ======================= ##
##
def print_dtype( data ):
    print_dtype_descr( data.dtype.descr )
   
## ======================= ##
##
def print_row( row ):
    print( str( row[ "reference_image" ] ) + ", " + str( row[ "image" ] ) + ", [" + str( row[ "is_cropped" ] ) + ", " + str( row[ "crop_x" ] ) + ", " + str( row[ "crop_y" ] ) + "]" )
   
## ======================= ##
##
def is_label_in( label, type ):

    for column in type.descr:
        if column[ 0 ] == label[ 0 ]:
            return True
    return False
    
## ======================= ##
##
def compute_additional_labels( type1, type2 ):
    
    additional_labels = list()
    
    for column in type2.descr:
        if not is_label_in( column, type1 ):
            additional_labels.append( column )
    
    return additional_labels

## ======================= ##
##
def row_is_less( row1, row2 ):

    if row1[ "reference_image" ] < row2[ "reference_image" ]:
        return True
    elif row1[ "reference_image" ] == row2[ "reference_image" ]:
        if row1[ "image" ] < row2[ "image" ]:
            return True
        elif row1[ "image" ] == row2[ "image" ]:    
            if row1[ "is_cropped" ] < row2[ "is_cropped" ]:
                return True
            elif row1[ "is_cropped" ] == row2[ "is_cropped" ]:
                if row1[ "crop_x" ] < row2[ "crop_x" ]:
                    return True
                elif row1[ "crop_x" ] == row2[ "crop_x" ]:    
                    if row1[ "crop_y" ] < row2[ "crop_y" ]:
                        return True

    return False
    

## ======================= ##
##
def is_row_equal( row1, row2 ):

    if row1[ "reference_image" ] != row2[ "reference_image" ]:
        return False
    if row1[ "image" ] != row2[ "image" ]:
        return False
        
    if row1[ "is_cropped" ] != row2[ "is_cropped" ]:
        return False

    if row1[ "crop_x" ] != row2[ "crop_x" ]:
        return False

    if row1[ "crop_y" ] != row2[ "crop_y" ]:
        return False

    return True

## ======================= ##
##
def find_row_idx( row, data, start_idx ):

    idx = start_idx
    
    while row_is_less( data[ idx ], row ):
        idx = idx + 1
        
    row2 = data[ idx ]
    
    if not is_row_equal( row, row2 ):
        print( "Rows don't match: " )
        print_row( row )
        print( "and")
        print_row( row2 )
        
        #assert( False )
        return -1
    
    return idx

    
## ======================= ##
##
def copy_content( data2, extended_dataset, additional_labels ):

    not_matched = []

    sec_idx = 0
    for idx in range( 0, extended_dataset.shape[ 0 ] ):
        
        sec_idx_tmp = find_row_idx( extended_dataset[ idx ], data2, sec_idx )
        
        if sec_idx_tmp >= 0:
        
            sec_idx = sec_idx_tmp
            
            # Copy data
            src_row = data2[ sec_idx ]
            dst_row = extended_dataset[ idx ]
            
            print_row( src_row )
            
            for column in additional_labels:
                dst_row[ column[ 0 ] ] = src_row[ column[ 0 ] ]
            
            sec_idx += 1
            
        else:
            not_matched.append( idx )
        
    print( "==========================================================" )
    print( "Number of not matched rows: " + str( len( not_matched ) ) )
            
    
## ======================= ##
##
def merge_datasets_new_metrics( data1, data2 ):
    
    print( "Computing dataset columns." )
    additional_labels = compute_additional_labels( data1.dtype, data2.dtype )
    
    print( "Additional columns to add to dataset:" )
    print_dtype_descr( additional_labels )
    print( "" )
    
    print( "Creating new array" )
    new_dtype = numpy.dtype( data1.dtype.descr + additional_labels )
    extended_dataset = numpy.zeros( data1.shape, dtype=new_dtype )

    print( "Sorting datasets" )
    sorting_order = [ "reference_image", "image", "is_cropped", "crop_x", "crop_y" ]
    
    print( "    Sorting first dataset..." )
    data1.sort( order=sorting_order )
    #numpy.set_printoptions(threshold=numpy.inf)
    #print( data1[ [ "reference_image", "image" ] ] )
    
    print( "    Sorting second dataset..." )
    data2.sort( order=sorting_order )
    #print( data2 )
    print( "    Sorting finished." )
    
    print( "Coping content to new array" )
    for name in data1.dtype.names:
        extended_dataset[ name ] = data1[ name ]
        
    print( "Coping new metrics to created array." )
    copy_content( data2, extended_dataset, additional_labels )
    
    return extended_dataset
    
    
## ======================= ##
##
def run():

    add_metrics_mode = "-add_metrics" in sys.argv
    add_rows_mode = "-add_rows" in sys.argv

    data = loading.load_dataset( sys.argv[ 1 ] )
    print_dtype( data )
    
    data2 = loading.load_dataset( sys.argv[ 2 ] )
    print_dtype( data2 )
    
    if add_metrics_mode and add_rows_mode:
        print( "Choose only one option:  -add_metrics, -add_rows" )
        exit()
    
    if add_metrics_mode:
        data = merge_datasets_new_metrics( data, data2 )
        print_dtype( data.dtype )
    elif add_rows_mode:
        data = merge_datasets( data, data2 )
        print_dtype( data.dtype )
    else:
        print( "Add one of flags: -add_metrics, -add_rows" )
        exit()
    
    loading.save_binary( data, sys.argv[ 3 ] )
    

if __name__ == "__main__":
    run()
    