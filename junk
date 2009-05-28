#!/usr/bin/env python

import SimpleXMLRPCServer
import datetime
import math
import pdb

import logging

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', filename='/var/log/tdsurface/surfaceadaptor.log',level=logging.DEBUG,)


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
        
        logging.info("logRealTime")
               
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
            logging.error(str(e))
            return 'FAIL'

        return 'OK'
        
    def version(self):
        return '1.0'
    
    def addMWDRealTime(self,name,timestamp,value):

        logging.info(str("Processing:"+str(name)+str(timestamp)+str(value)))        

        mwdrt = [name,timestamp.split('.')[0],value]
        
        log_file.write(str(mwdrt))
        log_file.write('\n')

        if mwdrt in last:
            logging.error(str('Duplicate Found! Ignoring'))            
            return 'Duplicate!'

        if name == '':
            logging.error(str("No Name!"))            
            return 'No Name!'
                
        #append to the back
        last.append(mwdrt)
        logging.info(str("buffer size:"+str(len(last))))        

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
                logging.info(str("Processing High Res Gamma Ray"))                
                kwargs['type'] = 'gammaray'
                kwargs['value'] =  ( math.pow(10.0,( 2.0 * float(value) ) / 10000.0 ) * 2.0 )
            elif name == 'gammaray_lowres':
                logging.info(str("Processing Low Res Gamma Ray"))                
                kwargs['type'] = 'gammaray'
                kwargs['value'] =  ( math.pow(10.0,( 2.0 * float(value) ) / 100.0 ) * 2.0 )
            elif name == 'temperature':
                kwargs['value'] =  ( float(value) * 500.0 ) / 10000.0
            else:
                logging.warning(str("WARNING: Did not convert value."))                

                
            t = ToolMWDRealTime(**kwargs)

            t.save()
        except Exception, e:
            logging.error(str(e))
        	
        logging.info(str("Final Value:"+kwargs))        

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
        logging.info(str("Creating slips object at: %s" % (str(kwargs['time_stamp']))))
        
        slips_object = Slip(**kwargs)
        
        #add it to the db
        slips_object.save()

        #add instance to server
        return 'OK'
        

from config import xmlrpc_server_address
from daemon import Daemon
import sys

class SurfaceAdaptorDaemon( Daemon ) :
	def run(self) :
		
		logging.info('Server Surface Adaptor Starting...')
				
		logging.info("Attempting to bind server to: %s" % xmlrpc_server_address)		
		
		try :
			server_object = XRServer()
			server = SimpleXMLRPCServer.SimpleXMLRPCServer((xmlrpc_server_address, 8888))
			server.register_instance(server_object)
		except Exception, e:
			logging.error(str(e))

		#Go into the main listener loop
		logging.info("Listening on port 8888")		
		server.serve_forever()
		
		
if __name__ == "__main__" :

	daemon = SurfaceAdaptorDaemon('/var/run/surfaceadaptor.pid')

	if len(sys.argv) == 2 :
		if 'start' == sys.argv[1] :
			daemon.start()
		elif 'stop' == sys.argv[1] :
			logging.info('Stopping Server')
			daemon.stop()
			
		elif 'restart' == sys.argv[1] :
			logging.info('Restarting Server')
			daemon.restart()
		else :
			print "Unknown command"
			print "usage: %s start|stop|restart" % sys.argv[0]
			sys.exit(2)
	
	elif len(sys.argv) == 1 :		
		daemon.start()
	
	else :
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
