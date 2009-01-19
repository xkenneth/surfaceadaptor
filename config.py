xmlrpc_server_protocol = 'http://'
xmlrpc_server_address = '10.0.1.190'
xmlrpc_server_port = '8888'
xmlrpc_server = "%s%s:%s" % (xmlrpc_server_protocol,xmlrpc_server_address, xmlrpc_server_port)

try:
    from config_local import *
except ImportError:
    pass
