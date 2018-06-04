import numpy
import matplotlib.pyplot
import sys



data_file = sys.argv[ 1 ]
data = numpy.recfromcsv( data_file, delimiter=',', names=True )
#data = data[ data[ "noise_peak" ] == True ]

xlabel = "ssim"
ylabel = "samples"

matplotlib.pyplot.scatter( data[ xlabel ], data[ ylabel ] )
matplotlib.pyplot.xlabel( xlabel )
matplotlib.pyplot.ylabel( ylabel )

matplotlib.pyplot.show()

#print( data )