import helpers
import os
from sys import argv
from PIL import Image

def wavlet_processor( image, parameters):

    command = ("convert {} \
     -wavelet-denoise {}% {}").format( image.filename, parameters.percent, "tmp.png" )
    os.system(command)
    img = Image.open("tmp.png")
    os.remove("tmp.png")
    return img

def run():
    parameters = []
    parameters_set = helpers.Parameters()
    parameters_set.percent = argv[3]
    parameters_set.file_postfix = "_" + argv[3]

    parameters.append(parameters_set)

    helpers.simple_process_directory(argv[1], argv[2], wavlet_processor, parameters)

if __name__ == "__main__":
    run()
