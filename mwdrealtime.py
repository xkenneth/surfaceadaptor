import sys

slips = False
if len(sys.argv) < 5:
    print "mwdrealtime.py type value timestamp"
    sys.exit()

import datetime

type = sys.argv[1]

value = float(sys.argv[2])

timestamp = " ".join(sys.argv[3:])

timestamp = timestamp.split('.')[0] #loses the microseconds!

timestamp = datetime.datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S")

print type, value, timestamp

import xmlrpclib
from config import xmlrpc_server

server = xmlrpclib.ServerProxy(xmlrpc_server)

server.addMWDRealTime(type,str(timestamp),value)
