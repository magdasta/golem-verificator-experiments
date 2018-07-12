import os
from enum import Enum
import re
from sys import argv
import numpy


class ShouldAccept(Enum):
    IGNORE = 3
    FALSE = 1
    DONT_KNOW = 2
    TRUE = 0


ok_thresholds = {
    "atom" : 1401,
    "barcelona" : 5125,
    "breakfast_room" : 3025,
    "bunkbed" : 6025,
    "car" : 1801,
    "cat" : 3825,
    "eco_light_bulb" : 1401,
    "french_woman" : 201,
    "glass" : 2900,
    "glass_material" : 4925,
    "habitacion" : 2825,
    "head" : 125,
    "interior" : 1001,
    "metal" : 425,
    "mug" : 3825,
    "office" : 3825,
    "plushy" : 4225,
    "ring" : 5725,
    "rocks" : 401,
    "sea" : 825,
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
    "ring" : 825,
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


def fix_windows_paths(path):
    return path.replace( "\\", "/" )

def get_scene_name(path):
    path = fix_windows_paths( path )
    scene = os.path.basename(os.path.dirname(path))
    if scene not in ok_thresholds.keys():
        raise Exception("Unknown scene '" + str( scene ) + "' (from path: " + str(path) + ")")
    return scene


def one_is_damaged(path_a, path_b):
    damaging_results = "damaging_results"
    return damaging_results in path_a or damaging_results in path_b


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

    if greater <= not_ok_thresholds[scene]:
        return ShouldAccept.IGNORE
    elif lesser >= ok_thresholds[scene]:
        return ShouldAccept.TRUE
    elif lesser <= not_ok_thresholds[scene] and greater >= ok_thresholds[scene]:
        return ShouldAccept.FALSE
    elif greater <= not_ok_thresholds[scene]:
        return ShouldAccept.IGNORE
    else:
        return ShouldAccept.DONT_KNOW


psnred = 0

def get_psnred():
    # global psnred
    return psnred

def should_accept(row):
    global psnred
    path_a = row["reference_image"].decode('UTF-8')
    path_b = row["image"].decode('UTF-8')

    if get_scene_name(path_a) != get_scene_name(path_b):
        throw_shouldnt_be_compared_exception(path_a, path_b)

    if row["psnr"] > 70:
        psnred = psnred + 1
        return ShouldAccept.TRUE
    if one_is_damaged(path_a, path_b):
        return ShouldAccept.FALSE
    elif both_are_not_damaged(path_a, path_b):
        return tell_from_samples(path_a, path_b)
    else: #should not get here anymore
        assert False
        return ShouldAccept.FALSE


# if __name__ == "__main__":
#     print(should_accept(argv[1], argv[2]))
