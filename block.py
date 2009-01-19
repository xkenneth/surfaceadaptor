import sys

slips = False
if len(sys.argv) != 2:
    raise Exception("First argument must be block position.")

try:
    pos = float(sys.argv[1])
except Exception, e: 
    print e
    raise Exception("There was an error converting the block position!")

import xmlrpclib
from config import xmlrpc_server

server = xmlrpclib.ServerProxy(xmlrpc_server)

server.addSlipsStatus(str(pos))





