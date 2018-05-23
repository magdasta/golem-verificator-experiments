import itk
import image_io as imio
from sys import argv


def RGB_to_luminance( input_image ):

    input_type = type( image )
    scalar_pixel_type = itk.Image[itk.UC, 2]
    
    luminance_filter_type = itk.RGBToLuminanceImageFilter[ input_type, scalar_pixel_type ]
    luminance_filter = luminance_filter_type.New()
    
    luminance_filter.SetInput( input_image )
    luminance_filter.Update()
    
    return luminance_filter.GetOutput()
    
    
image = imio.load_image( argv[ 1 ] )
filtered = RGB_to_luminance( image )
imio.save_image( argv[ 2 ], filtered )


