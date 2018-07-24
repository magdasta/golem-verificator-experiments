# merges two npys assuming one of them can have less rows and more metrics than the other
from sys import argv
from .loading import load_dataset


def find_missing_columns(bigger_npy, smaller_npy):
    # this function returns columns present in bigger_npy but not present in smaller_npy
    bigger_npy_headers = bigger_npy.dtype.names
    smaller_npy_headers = smaller_npy.dtype.names
    missing_columns = dict()
    for header in bigger_npy_headers:
        if header not in smaller_npy_headers:
            missing_columns[header] = []
    return missing_columns


def run(bigger_npy, smaller_npy):
    #bigger_npy = load_dataset(bigger_npy_path)
    #smaller_npy = load_dataset(smaller_npy_path)
    columns_to_be_added = find_missing_columns(bigger_npy, smaller_npy)

    image = "image"
    reference_image = "reference_image"
    crop_x = "crop_x"
    crop_y = "crop_y"

    for row in smaller_npy:
        pair_comp = [ r for r in bigger_npy if (r[image] == row[image] and r[reference_image] == row[reference_image]) or (r[image] == row[reference_image] and r[reference_image] == row[image])]
                                        # and r[crop_x] == row[crop_x]
                                        # and r[crop_y] == row[crop_y] ]
        print (pair_comp)
        for header in columns_to_be_added.keys():
            columns_to_be_added[header].append(corresponding_row[header])

    return columns_to_be_added



if __name__ == "__main__":
    run(argv[1], argv[2])