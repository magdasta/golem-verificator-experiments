import pywt
import numpy as np
import helpers
from sys import argv
from PIL import Image

def waveletSmooth(x, wavelet="db4", freq_idx=6, level=None, title=None):
    coeff = pywt.wavedec2(x, wavelet)
    
    for i, _ in enumerate(coeff[freq_idx]):
        coeff[freq_idx][i].fill(0)

    y = pywt.waverec2(coeff, wavelet)
    return y

def wavlet_processor( image, parameters):
    #original_cv = cv2.imread(sys.argv[1])
    original = np.asarray(image)

    blue = original[..., 0]
    green = original[..., 1]
    red = original[..., 2]
    processed_blue = waveletSmooth(blue, parameters.wavelet, parameters.freq_idx)
    processed_green = waveletSmooth(green, parameters.wavelet, parameters.freq_idx)
    processed_red = waveletSmooth(red, parameters.wavelet, parameters.freq_idx)
    processed = np.dstack((processed_blue, processed_green, processed_red))
    return Image.fromarray(np.uint8(processed))

def run():
    parameters = []
    parameters_set = helpers.Parameters()
    parameters_set.wavelet = argv[3]
    parameters_set.freq_idx = int(argv[4])
    parameters_set.file_postfix = "_" + argv[3] + "_level_" + argv[4]

    parameters.append(parameters_set)

    helpers.simple_process_directory(argv[1], argv[2], wavlet_processor, parameters)

if __name__ == "__main__":
    run()
