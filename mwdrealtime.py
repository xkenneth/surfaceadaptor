import sys

slips = False
if len(sys.argv) < 5:
    print "mwdrealtime.py type value timestamp"
    sys.exit()

import datetime

type = sys.argv[1]

value = float(sys.argv[2])

timestamp = []
for i in sys.argv[3:]:
    if len(i.split('.')) > 1:
        timestamp.append("".join(i.split('.')[0:-1]))
    else:
        timestamp.append(i)

#timestamp = ["".join(i.split('.')[0:-1]) for i in sys.argv[3:]]
print timestamp

timestamp = " ".join(timestamp)
print timestamp

timestamp = timestamp.split('.')[0] #loses the microseconds!

#6:00:00.000 PM 12/31/1903
timestamp = datetime.datetime.strptime(timestamp,"%I:%M:%S %p %m/%d/%Y")
import pdb
pdb.set_trace()

print type, value, timestamp

import xmlrpclib
from config import xmlrpc_server

server = xmlrpclib.ServerProxy(xmlrpc_server)

server.addMWDRealTime(type,str(timestamp),value)
