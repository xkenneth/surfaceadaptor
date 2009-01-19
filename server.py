import SimpleXMLRPCServer
import datetime

#setup the django environment
from django.core.management import setup_environ

from tdsurface import settings

setup_environ(settings)

#import the needed models

#setting up the slip model

from tdsurface.depth.models import Slip, Settings

db_settings = Settings()

#The server object
class XRServer:
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
        

server_object = XRServer()
server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8888))
server.register_instance(server_object)

#Go into the main listener loop
print "Listening on port 8888"
server.serve_forever()
