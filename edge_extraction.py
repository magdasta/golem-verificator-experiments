import itk
import image_io as imio
from sys import argv
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

    
#image = imio.load_image( argv[ 1 ] )

reader = itk.ImageFileReader.IF2.New(FileName=argv[1])
#luminance_image = preprocessing.RGB_to_luminance_float( image )
filtered = sobel_filter( reader, None )
imio.save_image( argv[ 2 ], filtered )


# variance = 2.0

# reader = itk.ImageFileReader.IF2.New(FileName=argv[1])
# filter = itk.CannyEdgeDetectionImageFilter.IF2IF2.New(
    # reader,
    # Variance=variance)
# outputCast = itk.RescaleIntensityImageFilter.IF2IUC2.New(
    # filter,
    # OutputMinimum=0,
    # OutputMaximum=255)
# imio.save_image( argv[ 2 ], outputCast )