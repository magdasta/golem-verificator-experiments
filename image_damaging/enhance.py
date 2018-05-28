# Usage: python enhance.py (brightness | contrast | color) path_to_source_images output_path factor
from PIL import ImageEnhance
from sys import argv
import helpers


def change_brightness(image, parameters):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(parameters.factor)


def change_contrast(image, parameters):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(parameters.factor)


def change_color_balance(image, parameters):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(parameters.factor)


def get_proper_processor():
    transformation = argv[1].upper()
    if transformation == "BRIGHTNESS":
        return change_brightness
    elif transformation == "CONTRAST":
        return change_contrast
    elif transformation == "COLOR":
        return change_color_balance
    raise Exception("Got " + argv[1] + " as the first argument. Allowed values are 'brightness', 'contrast' and 'color'")


def run():
    parameters = []
    parameters_set = helpers.Parameters()
    parameters_set.factor = float(argv[4])
    parameters_set.file_postfix = "_" + argv[1] + "_factor_" + str(parameters_set.factor).replace(".", "_")

    parameters.append(parameters_set)

    helpers.simple_process_directory(argv[2], argv[3], get_proper_processor(), parameters)


if __name__ == "__main__":
    run()
