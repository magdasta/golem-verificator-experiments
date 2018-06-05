import itk
import image_io as imio
from PIL import Image, ImageFilter
from sys import argv
import os
import preprocessing


## ====================================
##
def sobel_filter( image, parameters ):

    input_type = type( image.GetOutput() )

    pixel_type = itk.ctype( 'float' )
    image_type = itk.Image[ pixel_type, 2 ]
    
    sobel_filter_type = itk.SobelEdgeDetectionImageFilter[ input_type, image_type ]
    sobel_filter = sobel_filter_type.New()
    
    sobel_filter.SetInput( image )
    sobel_filter.Update()
    return preprocessing.float_to_RGB( sobel_filter )

 
## ====================================
##
def find_edges( image ):
    
    return image.filter( ImageFilter.FIND_EDGES )

 
#image = imio.load_image( argv[ 1 ] )

# reader = itk.ImageFileReader.IF2.New(FileName=argv[1])
# #luminance_image = preprocessing.RGB_to_luminance_float( image )
# filtered = sobel_filter( reader, None )
# imio.save_image( argv[ 2 ], filtered )




## ======================= ##
##
def run():

    # image = Image.open( argv[ 1 ] )
    # filtered = find_edges( image )
    # filtered.save( argv[ 2 ], "PNG" )

    variance = float( argv[ 3 ] )
    
    ( file, ext ) = os.path.splitext( argv[ 2 ] )
    target_file = file + "_[variance=" + str( variance ) + "]" + ext

    reader = itk.ImageFileReader.IF2.New(FileName=argv[1])
    filter = itk.CannyEdgeDetectionImageFilter.IF2IF2.New(
        reader,
        Variance=variance)
    outputCast = itk.RescaleIntensityImageFilter.IF2IUC2.New(
        filter,
        OutputMinimum=0,
        OutputMaximum=255)
    imio.save_image( target_file, outputCast )



if __name__ == "__main__":
    run()