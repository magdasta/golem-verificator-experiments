from PIL import Image
from loading import load_dataset
from numpy.lib.recfunctions import append_fields
import numpy
import os
from sys import argv

full_image_sizes = dict()


def add_variance_difference(data_file_path, output_path):
    data = load_dataset(data_file_path)
    variance_differences = [get_variance_difference(row) for row in data]
    output_data = append_fields(data, "variance_difference", variance_differences, usemask=False)
    numpy.save(output_path, output_data)


def get_variance_difference(row):
    reference_variance = row["reference_variance"]
    image_variance = row["image_variance"]
    return abs(reference_variance - image_variance)


def add_image_sizes(data_file_path, output_path, images_database_path):
    data = load_dataset(data_file_path)
    image_sizes = [get_number_of_pixels(row, images_database_path) for row in data]
    output_data = append_fields(data, "number_of_pixels", image_sizes, usemask=False)
    numpy.save(output_path, output_data)


def get_number_of_pixels(row, images_database_path):
    reference_file_path = get_image_path_on_local_machine(images_database_path, row["reference_image"])
    pixels_in_full_image = get_number_of_pixels_from_path(reference_file_path)
    if row["is_cropped"] == True:
        return pixels_in_full_image / 100
    else:
        return pixels_in_full_image


def get_number_of_pixels_from_path(image_path):
    if image_path not in full_image_sizes.keys():
        print("Reading " + image_path)
        reference_image = Image.open(image_path)
        width, height = reference_image.size
        full_image_sizes[image_path] = width * height
    return full_image_sizes[image_path]


def get_image_path_on_local_machine(images_database_path, path_from_data):
    rel_path = path_from_data.decode('utf-8').split("images_database")[-1] # text after the last occurrence of "images_database" in path
    rel_path = rel_path.replace("\\", "/").strip("/")
    return os.path.join(images_database_path, rel_path)


def run():
    column_name = argv[1].lower()
    if column_name == "number_of_pixels":
        add_image_sizes(argv[2], argv[3], argv[4])
    elif column_name == "variance_difference":
        add_variance_difference(argv[2], argv[3])
    else:
        print("Invalid column name: " + argv[1])


if __name__ == "__main__":
    run()