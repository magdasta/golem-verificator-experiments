import os
from enum import Enum
import re
from sys import argv


class ShouldAccept(Enum):
    FALSE = 0.
    DONT_KNOW = 0.5
    TRUE = 1.


ok_thresholds = {
    "atom" : 1401,
    "barcelona" : 4125,
    "breakfast_room" : 2825,
    "bunkbed" : 6025,
    "car" : 1001,
    "cat" : 2825,
    "eco_light_bulb" : 1401,
    "french_woman" : 201,
    "glass" : 2900,
    "glass_material" : 4925,
    "habitacion" : 2825,
    "head" : 125,
    "interior" : 1001,
    "metal" : 425,
    "mug" : 3825,
    "office" : 2825,
    "plushy" : 3225,
    "ring" : 5725,
    "rocks" : 401,
    "sea" : 525,
    "shark" : 1201,
    "toughship" : 3225,
    "tree" : 425
}

not_ok_thresholds = {
    "atom" : 601,
    "barcelona" : 725,
    "breakfast_room" : 825,
    "bunkbed" : 1825,
    "car" : 401,
    "cat" : 1125,
    "eco_light_bulb" : 601,
    "french_woman" : 1,
    "glass" : 800,
    "glass_material" : 1925,
    "habitacion" : 1325,
    "head" : 85,
    "interior" : 401,
    "metal" : 25,
    "mug" : 1125,
    "office" : 1425,
    "plushy" : 1125,
    "ring" : 3125,
    "rocks" : 1,
    "sea" : 25,
    "shark" : 601,
    "toughship" : 725,
    "tree" : 25
}


def extract_number_of_samples(filename):
    match = re.search("samples=[0-9]+", filename)
    if not match:
        raise Exception("Invalid filename: " + filename)
    return int(match.group(0)[8:])


def get_scene_name(path):
    scene = os.path.basename(os.path.dirname(path))
    if scene not in ok_thresholds.keys():
        raise Exception("Unknown scene '" + scene + "'")
    return scene


def both_are_damaged(path_a, path_b):
    damaging_results = "damaging_results"
    return damaging_results in path_a and damaging_results in path_b


def both_are_not_damaged(path_a, path_b):
    good = "good"
    return good in path_a and good in path_b


def throw_shouldnt_be_compared_exception(path_a, path_b):
    raise Exception("Images " + path_a + " and " + path_b + " shouldn't be compared.")


def tell_from_samples(path_a, path_b):
    scene = get_scene_name(path_a)
    samples_a = extract_number_of_samples(path_a)
    samples_b = extract_number_of_samples(path_b)
    lesser = min(samples_a, samples_b)
    greater = max(samples_a, samples_b)

    if lesser >= ok_thresholds[scene]:
        return ShouldAccept.TRUE
    elif lesser <= not_ok_thresholds[scene]:
        return ShouldAccept.FALSE
    else:
        return ShouldAccept.DONT_KNOW


def should_accept(path_a, path_b):
    if get_scene_name(path_a) != get_scene_name(path_b):
        throw_shouldnt_be_compared_exception(path_a, path_b)

    if both_are_damaged(path_a, path_b):
        #throw_shouldnt_be_compared_exception(path_a, path_b)
        return ShouldAccept.FALSE
    elif both_are_not_damaged(path_a, path_b):
        return tell_from_samples(path_a, path_b)
    else:
        return ShouldAccept.FALSE


if __name__ == "__main__":
    print(should_accept(argv[1], argv[2]))