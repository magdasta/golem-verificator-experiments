import itk
import os
from sys import argv


## ====================================
##
def _ensure_dir( file_path ):
    directory = os.path.dirname( file_path )
    if not os.path.exists( directory ):
        os.makedirs( directory )


pixelType = itk.UC
imageType = itk.Image[pixelType, 2]

readerType = itk.ImageFileReader[imageType]
writerType = itk.ImageFileWriter[imageType]

reader = readerType.New()
writer = writerType.New()

reader.SetFileName( argv[1] )
writer.SetFileName( argv[2] )

# Create empty file
_ensure_dir( argv[2] )
open( argv[2], 'a' ).close()


writer.SetInput( reader.GetOutput() )
writer.Update()