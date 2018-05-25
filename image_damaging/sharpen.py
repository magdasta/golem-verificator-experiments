from PIL import Image, ImageFilter
import sys
import os
import helpers


## ======================= ##
##
def sharpen( image, parameters ):

    return image.filter( ImageFilter.SHARPEN )
    
## ======================= ##
##
def sharpen_image( src_file, target_file ):

    image = Image.open( src_file )
    sharpened = sharpen( image, None )
    sharpened.save( target_file )


## ======================= ##
##
def sharpen_images( src_file, target_dir ):

    [file_name, extension] = os.path.splitext(os.path.basename(src_file))
    target_file = file_name + "_smoothed" + extension
    target_path = os.path.join(target_dir, target_file)

    sharpen_image(src_file, target_path)
    

## ======================= ##
##
def run():
    helpers.process_directory( sys.argv[1], sys.argv[2], sharpen_images )
    
## ======================= ##
##
if __name__ == "__main__":
    run()
    
    