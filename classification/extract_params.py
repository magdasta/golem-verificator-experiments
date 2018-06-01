import re


## ======================= ##
##
def find_parameters( file_name ):
    
    regex = r'\[([^\[\]]+)\]'
    return re.findall( regex, file_name )


## ======================= ##
##
def extract_params( file_name ):
    
    params_list = []
    
    params = find_parameters( file_name )
    for param in params:

        if param.find( "=" ) >= 0:
            
            ( name, value ) = param.split( "=" )
            params_list.append( ( name, value ) )
        else:
            params_list.append( ( param, "True" ) )
    
    return params_list

    
    
    
#line = "[param1=2]_[param2=34]_[noise]"
#params = extract_params( line )


#print( str( params ) )
