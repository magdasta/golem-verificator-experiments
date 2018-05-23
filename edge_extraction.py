import itk
import image_io as imio
from sys import argv
import preprocessing



def sobel_filter( image, parameters ):

    input_type = type( image )

    pixel_type = itk.ctype( 'unsigned char' )
    pixel_type_RGB = itk.RGBPixel[ pixel_type ]
    image_type_RGB = itk.Image[ pixel_type_RGB, 2 ]
    
    sobel_filter_type = itk.SobelEdgeDetectionImageFilter[ input_type, image_type_RGB ]
    sobel_filter = sobel_filter_type.New()
    
    sobel_filter.SetInput( image )
    return sobel_filter

    
image = imio.load_image( argv[ 1 ] )
filtered = sobel_filter( image, None )
imio.save_image( argv[ 2 ], filtered.GetOutput() )

