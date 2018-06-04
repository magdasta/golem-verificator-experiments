import numpy
import matplotlib.pyplot
import sys



data_file = sys.argv[ 1 ]
data = numpy.genfromtxt( data_file, delimiter=',', names=True )

#matplotlib.pyplot.plot( "samples", "ssim", data=data )
matplotlib.pyplot.scatter( data[ "samples" ], data[ "ssim" ] )
matplotlib.pyplot.show()

#print( data )