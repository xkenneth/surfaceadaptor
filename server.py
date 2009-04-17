import SimpleXMLRPCServer
import datetime
import math
import pdb

#last buffer
last_length = 50
#fifo
last = []

#setup the django environment
from django.core.management import setup_environ

from tdsurface import settings

setup_environ(settings)

#import the needed models

#setting up the slip model

from tdsurface.depth.models import Slip, Settings, BlockPosition, ToolMWDRealTime

db_settings = Settings()

#The server object
class XRServer:
    def addMWDRealTime(self,type,timestamp,value):

        mwdrt = [type,timestamp,value]

        if mwdrt in last:
            print '.',
            return 'Duplicate!'
        
        print ""
        #append to the back
        last.append(mwdrt)
        print "buffer size:",len(last)

        #pop the first
        if len(last) > last_length:
            last.pop(0)

        try:
            value = float(value)
            
            kwargs = {'run':db_settings.get_active_run(),
                  'time_stamp':timestamp}

            if type == 'gx':
                kwargs['type'] = 'G'
                kwargs['value_x'] = value
            elif type == 'gy':
                kwargs['type'] = 'G'
                kwargs['value_y'] = value
            elif type == 'gz':
                kwargs['type'] = 'G'
                kwargs['value_z'] = value
            elif type == 'hx':
                kwargs['type'] = 'H'
                kwargs['value_x'] = value
            elif type == 'hy':
                kwargs['type'] = 'H'
                kwargs['value_y'] = value
            elif type == 'hz':
                kwargs['type'] = 'H'
                kwargs['value_z'] = value
            else:
                kwargs['type'] = type
                kwargs['value'] = value
                
            if type == 'toolface':
                kwargs['value'] = (float(value)/10000.0)*360.0
            elif type == 'inclination':
                kwargs['value'] = (float(value)/10000.0)*180.0
            elif type == 'azimuth':
                kwargs['value'] = (float(value)/10000.0)*360.0
            elif type == 'gammaray':
                kwargs['value'] =  ( math.pow(10.0,( 2.0 * float(value) ) / 10.0 ) * 2.0 )
            elif type == 'temperature':
                kwargs['value'] =  ( float(value) * 500.0 ) / 10000.0
            else:
                print "WARNING: Did not convert value."
            
                
            t = ToolMWDRealTime(**kwargs)

            t.save()
        except Exception, e:
            print "ERROR:",e
            print e

        print "Final Value:",kwargs['type'],"@",kwargs['time_stamp'],"=",kwargs['value']

        return 'OK'
        
            
    def addBlockPosition(self,position):
        
        kwargs = {'run':db_settings.get_active_run(),
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
        kwargs = {'run':db_settings.get_active_run(),
                  'time_stamp':str(datetime.datetime.now()),
                  'status':slips}

        #create the object
        print "Creating slips object at: %s" % (str(kwargs['time_stamp']))
        slips_object = Slip(**kwargs)
        
        #add it to the db
        slips_object.save()

        #add instance to server
        return 'OK'
        

from config import xmlrpc_server_address
print "Attempting to bind server to: %s" % xmlrpc_server_address

server_object = XRServer()
server = SimpleXMLRPCServer.SimpleXMLRPCServer((xmlrpc_server_address, 8888))
server.register_instance(server_object)

#Go into the main listener loop
print "Listening on port 8888"
server.serve_forever()
