from sys import argv
import os
import helpers

def apply_watermark( src_path, results_directory, parameters ):
    [ file_name, extension ] = os.path.splitext( os.path.basename( src_path ) )
    dst_path = os.path.join( results_directory, file_name + "_watermarked" + extension )
    command = "composite -compose plus {0} {1} {2}".format( src_path,
                                                            parameters.watermark_filename,
                                                            dst_path )
    os.system( command )

def run():
    parameters = helpers.Parameters()
    parameters.watermark_filename = "watermark.png"
    helpers.process_directory( argv[1], argv[2], apply_watermark, parameters )

if __name__ == "__main__":
    run()
