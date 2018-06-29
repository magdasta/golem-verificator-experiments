import cv2
import numpy
import math

import sys

import loading



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

# Images
screen = None
mask = None

# Configuration
show_mask =  True


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
        
        if selected_crops[ tile_x ][ tile_y ]:
            selected_crops[ tile_x ][ tile_y ] = False
            print( "Deselected crop: [" + str( tile_x ) + "][" + str( tile_y ) + "]" )
        else:
            selected_crops[ tile_x ][ tile_y ] = True
            print( "Selected crop: [" + str( tile_x ) + "][" + str( tile_y ) + "]" )
  
  
## ======================= ##
##   
def apply_mask( image, selected_crops ):

    masked_image = image.copy();
    mask = image.copy();
    
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
    
    if show_mask:
        masked_image = cv2.addWeighted( mask, alpha, masked_image, 1 - alpha, 0 )
    
    return masked_image

    
## ======================= ##
##
def show_hide_mask():
    global show_mask
    show_mask = not show_mask


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
def load_row( data, row ):
    
    print( "Selected comparision:" )
    print( "    " + row[ "reference_image" ].decode('UTF-8')  )
    print( "    " + row[ "image" ].decode('UTF-8')  )
    
    # Find all crops rows
    crop_rows = data[ ( data[ "reference_image" ] == row[ "reference_image" ] ) & ( data[ "image" ] == row[ "image" ] ) ]
    
    fill_crops_selections( crop_rows )
    
    
## ======================= ##
##
def main_loop( data_path ):
    global screen

    data = loading.load_dataset( data_path )
    full_images = data[ data[ "is_cropped" ] == False ]
    first_row = full_images[ 0 ]
    
    load_row( data, first_row )
    
    image = cv2.imread( first_row[ "image" ].decode('UTF-8'), cv2.IMREAD_COLOR )
    screen = numpy.zeros( image.shape, numpy.uint8 )
    
    cv2.namedWindow( 'Crops labeling' )
    cv2.setMouseCallback( 'Crops labeling', mouse_select )
    
    while(1):
    
        screen = apply_mask( image, selected_crops )
    
        cv2.imshow( 'Crops labeling', screen )
        
        key = cv2.waitKey( 20 )
        if key == ord( 'm' ):
            show_hide_mask()
        elif key == 27:
            break

    cv2.destroyAllWindows()


## ======================= ##
##
def run():

    main_loop( sys.argv[ 1 ] )

        
        
if __name__ == "__main__":
    run()



