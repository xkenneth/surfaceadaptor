import sys
import xmlrpclib
from config import xmlrpc_server

server = xmlrpclib.ServerProxy(xmlrpc_server)

slips = False
if len(sys.argv) != 2:
    raise Exception("First argument must be slips status.")

if not sys.argv[1] in ('in','out'): raise Exception('Invalid value.')

status = sys.argv[1]

server.addSlipsStatus(status)
