import pywt
import numpy
from PIL import Image

import sys

def calculate_mse( coeff1, coeff2, low, high ):
    sum = 0
    num = 0
    for i in range( low, high ):
        sum += sum( ( coeff1[ i ] - coeff2[ i ] ) ** 2 )
        num += len( coeff1[ i ] - coeff2[ i ] )
    return sum / num

## ======================= ##
##
class MetricWavelet:

    ## ======================= ##
    ##
    def compute_metrics(this, image1, image2):

        image1 = image1.convert("RGB")
        image2 = image2.convert("RGB")

        np_image1 = numpy.array(image1)
        np_image2 = numpy.array(image2)

        coeff1 = pywt.wavedec2( np_image1, "db4" )
        coeff2 = pywt.wavedec2( np_image2, "db4" )

        len_div_3 = len( coeff1 ) / 3
        len_two_thirds = len( coeff1 ) * 2 / 3\

        result = dict()
        result[ "wavelet_low" ] = calculate_mse( coeff1, coeff2, 0, low_div_3 )
        result[ "wavelet_mid" ] = calculate_mse( coeff1, coeff2, low_div_3, len_two_thirds )
        result[ "wavelet_high" ] = calculate_mse( coeff1, coeff2, len_two_thirds, len( coeff1 ) )

        return result

    ## ======================= ##
    ##
    def get_labels(this):
        return [ "wavelet_low", "wavelet_mid", "wavelet_high" ]


def waveletSmooth(x, wavelet="db4", freq_idx=6, level=None, title=None):
    coeff = pywt.wavedec2(x, wavelet)

    for i, _ in enumerate(coeff[freq_idx]):
        coeff[freq_idx][i].fill(0)

    y = pywt.waverec2(coeff, wavelet)
    return y


def wavlet_processor(image, parameters):
    # original_cv = cv2.imread(sys.argv[1])
    original = np.asarray(image)

    blue = original[..., 0]
    green = original[..., 1]
    red = original[..., 2]
    processed_blue = waveletSmooth(blue, parameters.wavelet, parameters.freq_idx)
    processed_green = waveletSmooth(green, parameters.wavelet, parameters.freq_idx)
    processed_red = waveletSmooth(red, parameters.wavelet, parameters.freq_idx)
    processed = np.dstack((processed_blue, processed_green, processed_red))
    return Image.fromarray(np.uint8(processed))


## ======================= ##
##
def run():
    first_img = Image.open( sys.argv[1] )
    second_img = Image.open( sys.argv[2] )

    ssim = MetricWavelet()

    print(ssim.compute_metrics(first_img, second_img))


if __name__ == "__main__":
    run()
