import numpy
import matplotlib.pyplot
import sys





data_file = sys.argv[ 1 ]
data = numpy.recfromcsv( data_file, delimiter=',', names=True )


damage = data[ data[ "samples" ] != data[ "samples_reference" ] ]
diffrent_sampling = data[ data[ "samples" ] == data[ "samples_reference" ] ]


#print( diffrent_sampling )



damage = damage[ damage[ "is_cropped" ] == True ]
diffrent_sampling = diffrent_sampling[ diffrent_sampling[ "is_cropped" ] == True ]

xlabel = "reference_variance"
ylabel = "variance_diff"


matplotlib.pyplot.scatter( diffrent_sampling[ xlabel ], diffrent_sampling[ ylabel ] )
matplotlib.pyplot.scatter( damage[ xlabel ], damage[ ylabel ] )


matplotlib.pyplot.xlabel( xlabel )
matplotlib.pyplot.ylabel( ylabel )

matplotlib.pyplot.show()

#print( data )