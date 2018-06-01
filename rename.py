'''
Removes resolution and serial number from file names
'''
import os
from sys import argv


def simplify_file_name(file_name):
    split = file_name.split("_")
    samples_and_extension = split[-1]
    ( samples, extension ) = os.path.splitext( samples_and_extension )
    base_name = split[0]
    return base_name + "_[samples=" + samples + "]" + extension


def rename():
    source_images_directory = argv[1]
    for root, dirs, files in os.walk(source_images_directory):
        for file_name in files:
            new_file_name = simplify_file_name(file_name)
            os.rename(os.path.join(root, file_name), os.path.join(root, new_file_name))


if __name__ == "__main__":
    rename()