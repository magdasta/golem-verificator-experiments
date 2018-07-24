from sys import argv
from . import loading


def change_path_prefixes(data, prefix_to_remove, prefix_to_add):
    reference_image = "reference_image"
    image = "image"
    for row in data:
        reference_path_decoded = row[reference_image].decode()
        # if prefix_to_remove not in reference_path_decoded:
        #     raise Exception("'" + prefix_to_remove + "' not found in '" + reference_path_decoded + "'")
        row[reference_image] = reference_path_decoded.replace(prefix_to_remove, prefix_to_add).encode()
        image_path_decoded = row[image].decode()
        # if prefix_to_remove not in image_path_decoded:
        #     raise Exception("'" + prefix_to_remove + "' not found in '" + image_path_decoded + "'")
        row[image] = image_path_decoded.replace(prefix_to_remove, prefix_to_add).encode()


def run(original_npy_path, target_npy_path, prefix_to_remove, prefix_to_add):
    data = loading.load_dataset(original_npy_path)
    change_path_prefixes(data, prefix_to_remove, prefix_to_add)
    loading.save_binary(data, target_npy_path)


if __name__ == "__main__":
    run(argv[1], argv[2], argv[3], argv[4])