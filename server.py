import SimpleXMLRPCServer
import datetime
import math
import pdb

log_file = open('log.txt','w+')
log_file.write('Server Starting @ '+str(datetime.datetime.now()))
log_file.write('\n')

#last buffer
last_length = 150
#fifo
last = []

#setup the django environment
from django.core.management import setup_environ

from tdsurface import settings

setup_environ(settings)

#import the needed models

#setting up the slip model

from tdsurface.depth.models import Slip, Settings, BlockPosition, ToolMWDRealTime
from tdsurface.daq.models import ChannelLog

db_settings = Settings()

#The server object
class XRServer:
    def logRealTime(self,timestamp,types,values):
        
        log_file.write(str(timestamp))
        log_file.write('\n')

        values = values.split(',')
        types = types.split(',')

        ignore = ['us_flow_ready','depth_1','depth_2']

        #print types, values

        kwargs = {'well':db_settings.get_active_well(),
                  'time_stamp':timestamp}
        
        for i,t in enumerate(types):
            if t is not '' and t not in ignore:
                kwargs[t] = values[i]

        try:

            t = ChannelLog(**kwargs)
            
            t.save()
        except Exception, e:
            log_file.write(str(e))
            log_file.write('\n')
            return 'FAIL'

        return 'OK'
        
    def version(self):
        return '1.0'
    
    def addMWDRealTime(self,name,timestamp,value):

        log_file.write(str("Processing:"+str(name)+str(timestamp)+str(value)))
        log_file.write('\n')
        log_file.write(str(type(timestamp)))
        log_file.write('\n')

        mwdrt = [name,timestamp.split('.')[0],value]
        
        log_file.write(str(mwdrt))
        log_file.write('\n')

        if mwdrt in last:
            log_file.write(str('Duplicate Found! Ignoring'))
            log_file.write('\n')
            return 'Duplicate!'

        if name == '':
            log_file.write(str("No Name!"))
            log_file.write('\n')
            return 'No Name!'
        
        log_file.write(str(""))
        log_file.write('\n')
        #append to the back
        last.append(mwdrt)
        log_file.write(str("buffer size:"+str(len(last))))
        log_file.write('\n')

        #pop the first
        if len(last) > last_length:
            last.pop(0)

        try:
            value = float(value)
            
            kwargs = {'well':db_settings.get_active_well(),
                  'time_stamp':timestamp}

            if name == 'gx':
                kwargs['type'] = 'g'
                kwargs['value_x'] = value
            elif name == 'gy':
                kwargs['type'] = 'g'
                kwargs['value_y'] = value
            elif name == 'gz':
                kwargs['type'] = 'g'
                kwargs['value_z'] = value
            elif name == 'hx':
                kwargs['type'] = 'H'
                kwargs['value_x'] = value
            elif name == 'hy':
                kwargs['type'] = 'H'
                kwargs['value_y'] = value
            elif name == 'hz':
                kwargs['type'] = 'H'
                kwargs['value_z'] = value
            elif name == 'G':
                kwargs['type'] = 'g'
                kwargs['value'] = (float(value)/10000.0)*5.0
            elif name == 'H':
                kwargs['type'] = 'H'
                kwargs['value'] = (float(value)/10000.0)*5.0
            elif name == 'g':
                kwargs['type'] = 'g'
                kwargs['value'] = (float(value)/100.0)*5.0
            elif name == 'h':
                kwargs['type'] = 'H'
                kwargs['value'] = (float(value)/100.0)*5.0
            else:
                kwargs['type'] = name
                kwargs['value'] = value
                
            if name == 'toolface':
                kwargs['value'] = (float(value)/10000.0)*360.0
            elif name == 'inclination':
                kwargs['value'] = (float(value)/10000.0)*180.0
            elif name == 'azimuth':
                kwargs['value'] = (float(value)/10000.0)*360.0
            elif name == 'gammaray_highres':
                log_file.write(str("Processing High Res Gamma Ray"))
                log_file.write('\n')
                kwargs['type'] = 'gammaray'
                kwargs['value'] =  ( math.pow(10.0,( 2.0 * float(value) ) / 10000.0 ) * 2.0 )
            elif name == 'gammaray_lowres':
                log_file.write(str("Processing Low Res Gamma Ray"))
                log_file.write('\n')
                kwargs['type'] = 'gammaray'
                kwargs['value'] =  ( math.pow(10.0,( 2.0 * float(value) ) / 100.0 ) * 2.0 )
            elif name == 'temperature':
                kwargs['value'] =  ( float(value) * 500.0 ) / 10000.0
            else:
                log_file.write(str("WARNING: Did not convert value."))
                log_file.write('\n')
            
                
            t = ToolMWDRealTime(**kwargs)

            t.save()
        except Exception, e:
            log_file.write(str("ERROR:"+str(e)))
            log_file.write('\n')
            log_file.write(str(e))
            log_file.write('\n')

        log_file.write(str("Final Value:"+kwargs))
        log_file.write('\n')

        return 'OK'
        
            
    def addBlockPosition(self,position):
        
        kwargs = {'well':db_settings.get_active_well(),
                  'time_stamp':str(datetime.datetime.now()),
                  'position':str(position),
                  'position_units':'ft'}

        t = BlockPosition(**kwargs)

        t.save()

        return 'OK'

    def addSlipsStatus(self,status):
        #unpack xml
        slips = 0
        if status == 'in':
            slips = 1
        
        #setup the kwargs
        kwargs = {'well':db_settings.get_active_well(),
                  'time_stamp':str(datetime.datetime.now()),
                  'status':slips}

        #create the object
        log_file.write(str("Creating slips object at: %s" % (str(kwargs['time_stamp']))))
        log_file.write('\n')
        slips_object = Slip(**kwargs)
        
        #add it to the db
        slips_object.save()

        #add instance to server
        return 'OK'
        

from config import xmlrpc_server_address
log_file.write(str("Attempting to bind server to: %s" % xmlrpc_server_address))
log_file.write('\n')

server_object = XRServer()
server = SimpleXMLRPCServer.SimpleXMLRPCServer((xmlrpc_server_address, 8888))
server.register_instance(server_object)

#Go into the main listener loop
log_file.write(str("Listening on port 8888"))
log_file.write('\n')
server.serve_forever()
