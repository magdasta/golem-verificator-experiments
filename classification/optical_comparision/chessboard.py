# takes two images and creates a new one consisting of their fragments
from data_from_filename_extractor import extract_number_of_samples
import os
from PIL import Image
from sys import argv


BOX_SIZE = 200


def get_upper_left_corners(width, height):
    return [(x, y) for x in range(0, width, BOX_SIZE) for y in range(0, height, BOX_SIZE) if x % (BOX_SIZE * 2) == y % (BOX_SIZE * 2)]


def get_crop_boxes(size):
    width, height = size
    upper_left_corners = get_upper_left_corners(width, height)
    results = []
    for (left, top) in upper_left_corners:
        right = min(left + BOX_SIZE, width)
        bottom = min(top + BOX_SIZE, height)
        results.append((left, top, right, bottom))
    return results


def mix(path_a, path_b):
    image_a = Image.open(path_a)
    image_b = Image.open(path_b)
    if image_a.size != image_b.size:
        raise Exception("Image sizes differ")
    crop_boxes = get_crop_boxes(image_a.size)
    result = image_a.copy()
    for crop_box in crop_boxes:
        crop = image_b.crop(crop_box)
        result.paste(crop, crop_box)
    return result


def prepare_file_names_sorted_by_samples(files):
    result = []
    for file in files:
        result.append((extract_number_of_samples(file), file))
    return [filename for _, filename in sorted(result)]


def create_directory_if_doesnt_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


def prepare_output_file_name(results_directory, scene_folder, first_file_name, second_file_name):
    subdirectory_name = os.path.basename(scene_folder)
    base_name, extension = os.path.splitext(first_file_name)
    number_of_samples_in_second_file = extract_number_of_samples(second_file_name)
    new_file_name = base_name + "_compared_to_" + str(number_of_samples_in_second_file) + extension
    output_dirname = os.path.join(results_directory, subdirectory_name)
    create_directory_if_doesnt_exist(output_dirname)
    return os.path.join(output_dirname, new_file_name)


def make_chessboard_and_save(scene_folder, first_file_name, second_file_name, results_directory):
    first_image_path = os.path.join(scene_folder, first_file_name)
    second_image_path = os.path.join(scene_folder, second_file_name)
    chessboard = mix(first_image_path, second_image_path)
    result_path = prepare_output_file_name(results_directory, scene_folder, first_file_name, second_file_name)
    print("Saving: " + result_path)
    chessboard.save(result_path)


def run(source_images_directory, results_directory):
    for scene_folder, dirs, files in os.walk(source_images_directory):
        sorted_file_names = prepare_file_names_sorted_by_samples(files)
        number_of_images = len(sorted_file_names)
        for i in range(0, number_of_images - 1):
            make_chessboard_and_save(scene_folder, sorted_file_names[i], sorted_file_names[number_of_images - 1], results_directory)


if __name__ == "__main__":
    run(argv[1], argv[2])