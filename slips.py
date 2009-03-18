import sys
import xmlrpclib
from config import xmlrpc_server

print "Server: %s" % xmlrpc_server

print "Connecting."
server = xmlrpclib.ServerProxy(xmlrpc_server)
print "Connected."

slips = False
if len(sys.argv) != 2:
    raise Exception("First argument must be slips status.")

if not sys.argv[1] in ('in','out'): raise Exception('Invalid value.')

status = sys.argv[1]

print "Adding."
import pdb
pdb.set_trace()

server.addSlipsStatus(status)
