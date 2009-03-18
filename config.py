xmlrpc_server_protocol = 'http://'
xmlrpc_server_address = '192.168.15.144'
xmlrpc_server_port = '8888'
xmlrpc_server = "%s%s:%s" % (xmlrpc_server_protocol,xmlrpc_server_address, xmlrpc_server_port)

#WITS0 config
wits_baud = 9600
wits_timeout = 0.5
wits_device = '/dev/sd'


try:
    from config_local import *
except ImportError:
    pass
