### SYSTEM ###
import sys, time, datetime, os
#import elementtree.ElementTree as et
import getopt
import serial
import datetime

### MODULE ###
#import records
from PyWITS import globals
from PyWITS.wits0 import wits0

from config import wits_baud, wits_timeout, wits_device

ser = serial.Serial(wits_device,wits_baud,timeout=wits_timeout)
rec = wits0(ser)

#setup django ORM
from django.core.management import setup_environ
 
from tdsurface import settings
 
setup_environ(settings)

from tdsurface.depth.models import WITS0, Settings

while(1):
    try:
        
        print "Requesting Data"
        rec.write(globals.PASON_DATA_REQUEST)

        time.sleep(1)
        
        data = rec.read()
        
        if len(data) > 0:

            #log = et.fromstring('<log/>')
            
            #file_name = os.path.join(os.getcwd(),'wits_log.xml')
            #print "Logging to:",file_name
            #log_file = open(file_name,'a')
            
            print "Data Received"
            d = data[0]

            ts =  datetime.datetime.now()

            print ts

            #ts_element = et.Element('timestamp')
            #ts_element.text = str(ts)
            
            #log.append(ts_element)

            #open a log file

            for item in d.data_records:
                #item_element = et.Element('witsdata')
                #identifier_element = et.Element('identifier')
                #identifier_element.text = str(item.identifier.full)
                #item_element.append(identifier_element)
                
                #value_element = et.Element('value')
                #value_element.text = str(item.value)
                #item_element.append(value_element)
                
                #log.append(item_element)

                #if records.all.has_key(item.identifier.record_identifier):
                #    if records.all[item.identifier.record_identifier].has_key(item.identifier.item_identifier):
                #        print records.all[item.identifier.record_identifier][item.identifier.item_identifier]['description'],':',item.value
                #        continue
                
                print "Unkown data packet:", item

                #kwargs = {'run':settings.get_active_run(),
                #          'time_stamp':str(datetime.datetime.now()),
                #          'recid':item.identifier.record_identifier,
                #          'itemid':item.identifier.item_identifier,
                #          'value':str(item.value)}

                #WITS0(**kwargs)
                
                #add the data to the teledrill db
                
            #log_file.write(et.tostring(log)+'\n')
            #log_file.close()

            print "\n"*5
                    
        else:
            print "No Data Recieved, HAVE PATIENCE!"

        time.sleep(2)
        
    except KeyboardInterrupt:
        sys.exit()



