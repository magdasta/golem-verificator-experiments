import pywt
import numpy
from PIL import Image

import sys

def calculate_sum( coeff ):
    return sum( sum( coeff ** 2 ) )

def calculate_size( coeff ):
    shape = coeff.shape
    return shape[ 0 ] * shape[ 1 ]

def calculate_mse( coeff1, coeff2, low, high ):
    if low == high:
        if low == 0:
            high = low + 1
        else:
            low = high - 1
    suma = 0
    num = 0
    for i in range( low, high ):
        if type( coeff1[ i ] ) is tuple:
            suma += calculate_sum( coeff1[ i ][ 0 ] - coeff2[ i ][ 0 ] )
            suma += calculate_sum( coeff1[ i ][ 1 ] - coeff2[ i ][ 1 ] )
            suma += calculate_sum( coeff1[ i ][ 2 ] - coeff2[ i ][ 2 ] )
            num += 3 * coeff1[ i ][ 0 ].size
        else:
            suma += calculate_sum(coeff1[i] - coeff2[i] )
            num += coeff1[ i ].size
    if( num == 0 ):
        return 0
    else:
        return suma / num

## ======================= ##
##
class MetricWavelet:

    ## ======================= ##
    ##
    @staticmethod
    def compute_metrics( image1, image2):

        image1 = image1.convert("RGB")
        image2 = image2.convert("RGB")

        np_image1 = numpy.array(image1)
        np_image2 = numpy.array(image2)

        result = dict()
        result["wavelet_low"] = 0
        result["wavelet_mid"] = 0
        result["wavelet_high"] = 0

        for i in range(0,3):
            coeff1 = pywt.wavedec2( np_image1[...,i], "haar" )
            coeff2 = pywt.wavedec2( np_image2[...,i], "haar" )

            for l in range( len( coeff1 ) ):
                print( '({}, {}): {}'.format( str( i ), str( l ), calculate_mse( coeff1, coeff2, l, l+1 ) ) )

            len_div_3 = int( len( coeff1 ) / 3 )
            len_two_thirds = int( len( coeff1 ) * 2 / 3 )
            len_total = len( coeff1 )

            result[ "wavelet_low" ] = result[ "wavelet_low" ] + calculate_mse( coeff1, coeff2, 0, len_div_3 )
            result[ "wavelet_mid" ] = result[ "wavelet_mid" ] + calculate_mse( coeff1, coeff2, len_div_3, len_two_thirds )
            result[ "wavelet_high" ] = result[ "wavelet_high" ] + calculate_mse( coeff1, coeff2, len_two_thirds, len_total )

        return result

    ## ======================= ##
    ##
    @staticmethod
    def get_labels():
        return [ "wavelet_low", "wavelet_mid", "wavelet_high" ]


## ======================= ##
##
def run():
    first_img = Image.open( sys.argv[1] )
    second_img = Image.open( sys.argv[2] )

    ssim = MetricWavelet()

    print(ssim.compute_metrics(first_img, second_img))

    # print("croping...")
    #
    # middle = [ int( 0.5 * s ) for s in first_img.size ]
    #
    # first_crop = first_img.crop( [ 0, 0, middle[0], middle[1] ])
    # second_crop = second_img.crop( [ 0, 0, middle[0], middle[1] ])
    #
    # print(ssim.compute_metrics(first_crop, second_crop))


    print( "halving...")

    filter = Image.BILINEAR

    first_img = first_img.resize( [ int( 0.5 * s ) for s in first_img.size ], filter )
    second_img = second_img.resize( [ int( 0.5 * s ) for s in second_img.size ], filter )
    # first_img = first_img.resize( 0.5 * first_img.size )

    print(ssim.compute_metrics(first_img, second_img))

    # print( "halving...")
    #
    # first_img = first_img.resize( [ int( 0.5 * s ) for s in first_img.size ], filter )
    # second_img = second_img.resize( [ int( 0.5 * s ) for s in second_img.size ], filter )
    # # first_img = first_img.resize( 0.5 * first_img.size )
    #
    # print(ssim.compute_metrics(first_img, second_img))
    #
    # print( "halving...")
    #
    # first_img = first_img.resize( [ int( 0.5 * s ) for s in first_img.size ], filter )
    # second_img = second_img.resize( [ int( 0.5 * s ) for s in second_img.size ], filter )
    # # first_img = first_img.resize( 0.5 * first_img.size )
    #
    # print(ssim.compute_metrics(first_img, second_img))


if __name__ == "__main__":
    run()
