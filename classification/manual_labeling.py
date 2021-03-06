import cv2
import numpy
import math

import sys

import loading
import optical_comparision.chessboard as chessboard
import optical_comparision.should_accept as should_accept
import data_filtering



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
        
        if selected_crops[ tile_x ][ tile_y ] != TrueLabel:
            selected_crops[ tile_x ][ tile_y ] = TrueLabel
            print( "Selected crop: [" + str( tile_x ) + "][" + str( tile_y ) + "]" )
        else:
            selected_crops[ tile_x ][ tile_y ] = FalseLabel
            print( "Deselected crop:   [" + str( tile_x ) + "][" + str( tile_y ) + "]" )
  
  
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

## ======================= ##
##
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

scene_names = None

## ======================= ##
##
def compute_row_and_same_samples_crops_idx( data ):

    mask = ( data[ "reference_image" ] == current_row[ "reference_image" ] ) & ( data[ "image" ] == current_row[ "image" ] )
    return numpy.where( mask )[ 0 ]

## ======================= ##
##
def compute_row_and_all_crops_idx( data ):

    filtered_mask = data["samples"] != data["samples_reference"]

    scene = should_accept.get_scene_name( current_row[ "image" ].decode('UTF-8') )

    scene_mask = [scene_name == scene for scene_name in scene_names]

    return numpy.where( filtered_mask & scene_mask )[ 0 ]

## ======================= ##
##
def compute_current_row_idx( data ):

    indicies = compute_row_and_crops_idx( data )
    for idx in indicies:
        if data[ idx ][ "is_cropped" ] == False:
            return idx

    assert False, "Can't find fullscreen image."
    return -1
        
        
## ======================= ##
##
def update_crops_selection( data, config ):
    if config.filter_threshold:
        indicies = compute_row_and_all_crops_idx( data )
    else:
        indicies = compute_row_and_same_samples_crops_idx( data )

    scene = should_accept.get_scene_name( current_row[ "image" ].decode('UTF-8') )

    for idx in indicies:
        
        row = data[ idx ]
        if row[ "is_cropped" ]:
        
            tile_x = row[ "crop_x" ]
            tile_y = row[ "crop_y" ]

            label = selected_crops[ tile_x ][ tile_y ]
            if label == FalseLabel:
                data[ idx ][ "label" ] = get_label_string( should_accept.tell_from_samples( row[ "image" ].decode('UTF-8'), row[ "reference_image"].decode('UTF-8') ).value )
            elif label == TrueLabel:
                threshold = should_accept.not_ok_thresholds[ scene ]
                if row[ "samples"] >= threshold and row[ "samples_reference" ] >= threshold:
                    data[ idx ][ "label" ] = b"TRUE"
                else:
                    data[ idx ][ "label" ] = b"IGNORE"
            else:
                pass

## ======================= ##
##
def load_row( data, row ):
    global image
    global current_row
    
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

    print( "Help:\n" )
    
    print( "Labeling:" )
    print( "Green       - TRUE" )
    print( "Blue        - FALSE" )
    print( "Yellow      - DONT_KNOW" )
    print( "Red         - IGNORE\n" )
    
    print( "Key h - Print help." )
    print( "Key a - load image from previous row." )
    print( "Key d - load image from next row." )
    print( "Key m - Show/Hide labels." )
    print( "Key l - Show/Hide grid lines." )
    print( "Key Enter - Save dataset labeling.")
    print( "Press Escape to exit." )

    
## ======================= ##
##
def print_row( row ):
    
    feature_max_len = 40
    
    names = row.dtype.names
    for name in names:
        
        length = len( name )
        num_spaces = feature_max_len - length
        spaces_str = " " * num_spaces
        
        print(name + spaces_str + str(row[name]))
    
    
## ======================= ##
##
def print_current_row():

    print_row( current_row )
    

## ======================= ##
##
def select_scenes_with_threshold( data ):
    print( "Selecting scenes on subsampling threshold." )
    
    filtered = data[ data[ "samples" ] != data[ "samples_reference" ] ]
    
    # Create mask with all values False
    mask = filtered[ "samples" ] == 0
    
    scene_names_filtered = [ should_accept.get_scene_name( row[ "image" ].decode( 'UTF-8' ) ) for row in filtered ]
    
    for i, scene in enumerate( should_accept.ok_thresholds ):
        
        print( "Finding images on threshold for scene: " + scene )
        
        compared_ok_mask = ( filtered[ "samples" ] == should_accept.ok_thresholds[ scene ] ) & ( filtered[ "samples_reference" ] == should_accept.not_ok_thresholds[ scene ] )
        reference_ok_mask = ( filtered[ "samples_reference" ] == should_accept.ok_thresholds[ scene ] ) & ( filtered[ "samples" ] == should_accept.not_ok_thresholds[ scene ] )

        scene_mask = [ scene_name == scene for scene_name in scene_names_filtered ]
        
        threshold_mask = ( compared_ok_mask | reference_ok_mask )
        scene_threshold_mask = ( threshold_mask & scene_mask )
        
        mask = mask | scene_threshold_mask

    return filtered[ mask ]
        
    
## ======================= ##
##
def select_rows( data, config ):

    full_images = data[ data[ "is_cropped" ] == False ]

    if config.subsampling:
        return full_images[ full_images[ "samples_reference" ] != full_images[ "samples" ] ]
    elif config.filter_threshold:
        return select_scenes_with_threshold( full_images )
    else:
        return full_images


esc_pressed = False

## ======================= ##
##
def main_loop( config ):
    global screen
    global esc_pressed
    global scene_names

    data = loading.load_dataset( config.dataset )
    full_images = select_rows( data, config )
    
    scene_names = [ should_accept.get_scene_name( row[ "image" ].decode( 'UTF-8' ) ) for row in data ]

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
            update_crops_selection( data, config )
            load_next_row( data, full_images )
        elif key == ord( 'a' ):
            update_crops_selection( data, config )
            load_previous_row( data, full_images )
        elif key == ord( "h" ):
            print_help()
        elif key == ord( "l" ):
            show_grid_lines()
        elif key == ord( "\r" ):
            update_crops_selection( data, config )
            data_filtering.save_binary( data, config.dataset )
        elif key == ord( "y" ):
            if esc_pressed:
                update_crops_selection( data, config )
                data_filtering.save_binary( data, config.dataset )
                break
            else:
                pass
        elif key == ord( "n" ):
            if esc_pressed:
                break
            else:
                pass
        elif key == 27:
            print( "Do you want to save your dataset labeling? (y/n)")
            esc_pressed = True

    cv2.destroyAllWindows()

    
## ======================= ##
##
def parse_configuration():
    
    config = Config()
    config.dataset = sys.argv[ 1 ]
    config.subsampling = "-subsampling" in sys.argv
    config.filter_threshold = "-filter_threshold" in sys.argv
    
    
    return config
    
    
## ======================= ##
##
def run():

    config = parse_configuration()
    main_loop( config )

        
        
if __name__ == "__main__":
    run()



