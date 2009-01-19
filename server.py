import SimpleXMLRPCServer
import datetime

#setup the django environment
from django.core.management import setup_environ

from tdsurface import settings

setup_environ(settings)

#import the needed models

#setting up the slip model

from tdsurface.depth.models import Slip, Settings, BlockPosition, MWDRealTime

db_settings = Settings()

#The server object
class XRServer:
    def addMWDRealTime(self,type,timestamp,value):

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

        t = MWDRealTime(**kwargs)

        t.save()

        return 'OK'
        
            
    def addBlockPosition(self,position):
        
        kwargs = {'run':db_settings.get_active_run(),
                  'time_stamp':datetime.datetime.now(),
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
                  'time_stamp':datetime.datetime.now(),
                  'status':slips}

        #create the object
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
