import cv2
import numpy
import math

import sys


## ======================= ##
##
tiles = 10
selected_crops = numpy.zeros( ( tiles, tiles ), numpy.uint8 )
screen = None
mask = None


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
            print( "Selected crop: [" + str( tile_x ) + "][" + str( tile_y ) + "]" )
        else:
            selected_crops[ tile_x ][ tile_y ] = True
            print( "Deselected crop: [" + str( tile_x ) + "][" + str( tile_y ) + "]" )
  
  
## ======================= ##
##   
def apply_mask( image, selected_crops ):

    masked_image = image.copy();
    mask = image.copy();
    
    for tile_x in range( 0, selected_crops.shape[ 0 ] ):
        for tile_y in range( 0, selected_crops.shape[ 1 ] ):
        
            if selected_crops[ tile_x ][ tile_y ]:
                
                box = crop_to_box( tile_x, tile_y )
                cv2.rectangle( mask, ( box[ 0 ], box[ 1 ] ), ( box[ 2 ], box[ 3 ] ), ( 255, 0, 0 ), thickness = cv2.FILLED )
                
    
    alpha = 0.6
    masked_image = cv2.addWeighted( mask, alpha, masked_image, 1 - alpha, 0 )
    
    return masked_image

    
    
## ======================= ##
##
def main_loop( image_path ):
    global screen

    image = cv2.imread( image_path, cv2.IMREAD_COLOR )
    screen = numpy.zeros( image.shape, numpy.uint8 )
    
    cv2.namedWindow( 'Crops labeling' )
    cv2.setMouseCallback( 'Crops labeling', mouse_select )
    
    while(1):
    
        screen = apply_mask( image, selected_crops )
    
        cv2.imshow( 'Crops labeling', screen )
        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()


## ======================= ##
##
def run():

    main_loop( sys.argv[ 1 ] )

        
        
if __name__ == "__main__":
    run()



