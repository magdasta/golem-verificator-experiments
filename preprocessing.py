import itk
import image_io as imio
from sys import argv



## ====================================
##
def RGB_to_luminance( input_image ):

    input_type = type( input_image )
    scalar_pixel_type = itk.Image[itk.UC, 2]
    
    luminance_filter_type = itk.RGBToLuminanceImageFilter[ input_type, scalar_pixel_type ]
    luminance_filter = luminance_filter_type.New()
    
    luminance_filter.SetInput( input_image )
    luminance_filter.Update()
    
    return luminance_filter.GetOutput()
    
## ====================================
##
def float_to_RGB( input_image ):

    rescaler = itk.RescaleIntensityImageFilter.IF2IUC2.New( input_image, OutputMinimum=0, OutputMaximum=255 )
    rescaler.Update()
    
    return rescaler.GetOutput()
    