ignore = ['us_flow_ready','depth_1','depth_2']

#axis = ['x','y','z']

def convert(name, value):
    
    name, axis, res = name.split('_')
    
    if name in ['gravity','magnetic']:
        if res == 'highres':
            value = (float(value)/10000.0)*5.0
        elif res == 'lowres':
            value = (float(value)/100.0)*5.0

    elif name == 'toolface':
        value = (float(value)/10000.0)*360.0

    elif name == 'toolface':
        value = (float(value)/10000.0)*360.0
        
    elif name == 'inclination':
        value = (float(value)/10000.0)*180.0

    elif name == 'azimuth':
        value = (float(value)/10000.0)*360.0

    elif name == 'gammaray':
        if res == 'highres':
            value = ( math.pow(10.0,( 2.0 * float(value) ) / 10000.0 ) * 2.0 )
        elif res == 'lowres':
            value = ( math.pow(10.0,( 2.0 * float(value) ) / 100.0 ) * 2.0 )

    elif name == 'temperature':
        value = ( float(value) * 500.0 ) / 10000.0
        
    
    return name, axis, value
        
        
    
