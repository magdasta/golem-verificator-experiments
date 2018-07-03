import cv2
import numpy
import math

import sys

import loading
import optical_comparision.chessboard as chessboard
import optical_comparision.should_accept as should_accept



## ======================= ##
##
class Config:
    pass
    

## ======================= ##
##
tiles = 10
selected_crops = numpy.zeros( ( tiles, tiles ), numpy.uint8 )

TrueLabel = 0
FalseLabel = 1
DontKnowLabel = 2
IgnoreLabel = 3

TrueColor = ( 0, 255, 0 )
FalseColor = ( 255, 0, 0 )
DontKnowColor = ( 0, 200, 200 )
IgnoreColor = ( 0, 0, 255 )


current_row_idx = -1
current_row = None

# Images
screen = None
mask = None

# Configuration
show_mask =  True
show_grid = False


## ======================= ##
##
def position_to_crop( x, y ):

    width = screen.shape[ 1 ]
    height = screen.shape[ 0 ]
        
    crop_width = width / tiles
    crop_height = height / tiles
    
    tile_x = math.floor( x / crop_width )
    tile_y = math.floor( y / crop_height )
    
    return ( tile_x, tile_y )


## ======================= ##
##
def crop_to_box( tile_x, tile_y ):

    width = screen.shape[ 1 ]
    height = screen.shape[ 0 ]
        
    crop_width = width / tiles
    crop_height = height / tiles
    
    crop_x = tile_x * crop_width
    crop_y = tile_y * crop_height
    
    box = [ int( crop_x ), int( crop_y ), int( crop_x + crop_width ), int( crop_y + crop_height ) ]
    
    return box


## ======================= ##
##
def mouse_select( event, x, y, flags, param ):
    global selected_crops

    if event == cv2.EVENT_LBUTTONDOWN:
        
        ( tile_x, tile_y ) = position_to_crop( x, y )
        
        if selected_crops[ tile_x ][ tile_y ] != FalseLabel:
            selected_crops[ tile_x ][ tile_y ] = FalseLabel
            print( "Deselected crop: [" + str( tile_x ) + "][" + str( tile_y ) + "]" )
        else:
            selected_crops[ tile_x ][ tile_y ] = IgnoreLabel
            print( "Selected crop:   [" + str( tile_x ) + "][" + str( tile_y ) + "]" )
  
  
## ======================= ##
##   
def apply_mask( image, selected_crops ):

    masked_image = image.copy();
    mask = image.copy();
    
    if show_mask:
        for tile_x in range( 0, selected_crops.shape[ 0 ] ):
            for tile_y in range( 0, selected_crops.shape[ 1 ] ):
            
                box = crop_to_box( tile_x, tile_y )
                
                if selected_crops[ tile_x ][ tile_y ] == FalseLabel:
                    cv2.rectangle( mask, ( box[ 0 ], box[ 1 ] ), ( box[ 2 ], box[ 3 ] ), FalseColor, thickness = cv2.FILLED )
                elif selected_crops[ tile_x ][ tile_y ] == TrueLabel:
                    cv2.rectangle( mask, ( box[ 0 ], box[ 1 ] ), ( box[ 2 ], box[ 3 ] ), TrueColor, thickness = cv2.FILLED )
                elif selected_crops[ tile_x ][ tile_y ] == DontKnowLabel:
                    cv2.rectangle( mask, ( box[ 0 ], box[ 1 ] ), ( box[ 2 ], box[ 3 ] ), DontKnowColor, thickness = cv2.FILLED )
                elif selected_crops[ tile_x ][ tile_y ] == IgnoreLabel:
                    cv2.rectangle( mask, ( box[ 0 ], box[ 1 ] ), ( box[ 2 ], box[ 3 ] ), IgnoreColor, thickness = cv2.FILLED )
        
        alpha = 0.6
        masked_image = cv2.addWeighted( mask, alpha, masked_image, 1 - alpha, 0 )
    
    return masked_image

## ======================= ##
##
def draw_grid_lines( image ):

    if show_grid:
        
        # vertical
        for tile in range( 1, tiles ):
            box = crop_to_box( tile, 0 )
            cv2.line( image, ( box[ 0 ], 0 ), ( box[ 0 ], image.shape[ 0 ] ), ( 255, 255, 255 ) )
            
        # horizontal
        for tile in range( 1, tiles ):
            box = crop_to_box( 0, tile )
            cv2.line( image, ( 0, box[ 1 ] ), ( image.shape[ 1 ], box[ 1 ] ), ( 255, 255, 255 ) )

    
## ======================= ##
##
def show_hide_mask():
    global show_mask
    show_mask = not show_mask

## ======================= ##
##
def show_grid_lines():
    global show_grid
    show_grid = not show_grid
    
    
## ======================= ##
##
def get_label( row ):
    
    label = row[ "label" ]
    if label == b"TRUE":
        return TrueLabel
    elif label == b"FALSE":
        return FalseLabel
    elif label == b"DONT_KNOW":
        return DontKnowLabel
    else:
        return IgnoreLabel

    
## ======================= ##
##
def fill_crops_selections( crop_rows ):
    global selected_crops

    selected_crops = numpy.zeros( ( tiles, tiles ), numpy.uint8 )

    for row in crop_rows:
        
        tile_x = row[ "crop_x" ]
        tile_y = row[ "crop_y" ]
        
        selected_crops[ tile_x ][ tile_y ] = get_label( row )

def get_label_string( label ):
    if label == TrueLabel:
        return b"TRUE"
    elif label == FalseLabel:
        return b"FALSE"
    elif label == DontKnowLabel:
        return b"DONT_KNOW"
    elif label == IgnoreLabel:
        return b"IGNORE"
    else:
        assert False

def update_crops_selection( data ):
    index = current_row_idx + 1
    for y in range( tiles ):
        for x in range( tiles ):
            data[ index ][ "label" ] = get_label_string( selected_crops[ y ][ x ] )
            index = index + 1

## ======================= ##
##
def load_row( data, row ):
    global image
    
    print( "Selected comparision:" )
    print( "    " + row[ "reference_image" ].decode('UTF-8')  )
    print( "    " + row[ "image" ].decode('UTF-8')  )
    
    # Find all crops rows
    crop_rows = data[ ( data[ "reference_image" ] == row[ "reference_image" ] ) & ( data[ "image" ] == row[ "image" ] ) ]
    fill_crops_selections( crop_rows )
    
    # load image
    image = chessboard.chessboard_from_csv( row )
    current_row = row
    
    
## ======================= ##
##
def load_next_row( data, full_images ):
    global current_row_idx

    current_row_idx = current_row_idx + 1
    if current_row_idx >= len( full_images ):
        current_row_idx = 0

    first_row = full_images[ current_row_idx ]
    load_row( data, first_row )

    
## ======================= ##
##
def load_previous_row( data, full_images ):
    global current_row_idx

    current_row_idx = current_row_idx - 1
    if current_row_idx < 0:
        current_row_idx = len( full_images ) - 1

    first_row = full_images[ current_row_idx ]
    load_row( data, first_row )

    
## ======================= ##
##
def print_help():

    print( "Help:" )
    print( "Key h - Print help." )
    print( "Key a - load image from previous row." )
    print( "Key d - load image from next row." )
    print( "Key m - Show/Hide labels." )
    print( "Key l - Show/Hide grid lines." )
    print( "Press Escape to exit." )

    
# ## ======================= ##
# ##
# def select_scenes_with_threshold( data ):
    
    # print( "Selecting scenes on subsampling threshold." )
    
    # for i, scene in enumerate( should_accept.ok_thresholds ):
        
        # not_ok_mask = ( data[ "samples" ] == should_accept.not_ok_thresholds[ scene ] ) | ( data[ "samples_reference" ] == should_accept.not_ok_thresholds[ scene ] )
        # ok_mask = ( data[ "samples_reference" ] == should_accept.ok_thresholds[ scene ] ) | ( data[ "samples" ] == should_accept.ok_thresholds[ scene ] )

        # filtered = 
        
        
    
## ======================= ##
##
def select_rows( data, config ):

    full_images = data[ data[ "is_cropped" ] == False ]

    if config.subsampling:
        return full_images[ full_images[ "samples_reference" ] != full_images[ "samples" ] ]
    else:
        return full_images

    
## ======================= ##
##
def main_loop( config ):
    global screen

    data = loading.load_dataset( config.dataset )
    full_images = select_rows( data, config )
    
    load_next_row( data, full_images )

    screen = numpy.zeros( image.shape, numpy.uint8 )
    
    cv2.namedWindow( 'Crops labeling' )
    cv2.setMouseCallback( 'Crops labeling', mouse_select )
    
    while(1):
    
        screen = apply_mask( image, selected_crops )
        draw_grid_lines( screen )
    
        cv2.imshow( 'Crops labeling', screen )
        
        key = cv2.waitKey( 20 )
        if key == ord( 'm' ):
            show_hide_mask()
        elif key == ord( 'd' ):
            update_crops_selection( data )
            load_next_row( data, full_images )
        elif key == ord( 'a' ):
            update_crops_selection( data )
            load_previous_row( data, full_images )
        elif key == ord( "h" ):
            print_help()
        elif key == ord( "l" ):
            show_grid_lines()
        elif key == 27:
            break

    cv2.destroyAllWindows()

    
## ======================= ##
##
def parse_configuration():
    
    config = Config()
    config.dataset = sys.argv[ 1 ]
    config.subsampling = "-subsampling" in sys.argv
    
    
    return config
    
    
## ======================= ##
##
def run():

    config = parse_configuration()
    main_loop( config )

        
        
if __name__ == "__main__":
    run()



