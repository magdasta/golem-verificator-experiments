from sys import argv
import os
from PIL import Image
import random


def is_valid_image_file(file_name):
    return (file_name.endswith(".png") or file_name.endswith(".jpg")) \
           or file_name.endswith(".jpeg") or file_name.endswith(".exr") \
           and "output" not in file_name


def get_at_x_y(pixels, width, x, y):
    return pixels[width * y + x]


def get_random_channels_order(pixel):
    channels_order = list(range(len(pixel)))
    while channels_order == sorted(channels_order):
        random.shuffle(channels_order)
    return channels_order


def convert_image(image, path_out, channels_order):
    width, height = image.size
    pixels = image.getdata()
    converted = image.copy()

    for x in range(width):
        for y in range(height):
            pixel = get_at_x_y(pixels, width, x, y)
            new_pixel = []
            for channel in channels_order:
                new_pixel.append(pixel[channel])
            converted.putpixel((x, y), tuple(new_pixel))
    print(path_out)
    converted.save(path_out)


def channels_order_to_string(channels_order):
    return "".join(str(channel) for channel in channels_order)


def prepare_output_file_name(results_directory, subdirectory_name, file_name, channels_order):
    base_name, extension = os.path.splitext(file_name)
    file_name = base_name + "_channels_" + channels_order_to_string(channels_order) + extension
    return os.path.join(results_directory, subdirectory_name, file_name)


def create_directory_if_doesnt_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


def run():
    source_images_directory = argv[1]
    results_directory = argv[2]
    create_directory_if_doesnt_exist(results_directory)
    for root, dirs, files in os.walk(source_images_directory):
        subdirectory_name = (os.path.basename(root))
        channels_order = []
        for file_name in files:
            if is_valid_image_file(file_name):
                path_in = os.path.join(root, file_name)
                image = Image.open(path_in)
                if not channels_order:
                    channels_order = get_random_channels_order(image.getdata()[0])
                create_directory_if_doesnt_exist(os.path.join(results_directory, subdirectory_name))
                convert_image(image,
                              prepare_output_file_name(results_directory, subdirectory_name, file_name, channels_order)
                              , channels_order)


if __name__ == "__main__":
    run()