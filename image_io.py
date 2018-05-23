import itk
import os
from sys import argv


## ====================================
##
def _ensure_dir( file_path ):
    directory = os.path.dirname( file_path )
    if not os.path.exists( directory ):
        os.makedirs( directory )

## ====================================
##
def load_image( file_path ):

    pixelType = itk.UC
    imageType = itk.Image[pixelType, 2]

    readerType = itk.ImageFileReader[ imageType ]
    reader = readerType.New()
    
    reader.SetFileName( file_path )
    return reader

## ====================================
##
def save_image( file_path, image ):
    
    pixelType = itk.UC
    imageType = itk.Image[pixelType, 2]

    writerType = itk.ImageFileWriter[imageType]
    writer = writerType.New()

    writer.SetFileName( argv[2] )
        
    # Create empty file
    _ensure_dir( argv[2] )
    open( argv[2], 'a' ).close()
    
    writer.SetInput( image )
    writer.Update()
    


reader = load_image( argv[ 1 ] )
save_image( argv[ 2 ], reader.GetOutput() )