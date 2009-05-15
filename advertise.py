import pybonjour
import select
import logging

def register():
    name    = 'surface_adaptor'
    regtype = '_surface_adaptor._tcp'
    port    = 8888


    def register_callback(sdRef, flags, errorCode, name, regtype, domain):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            print 'Registered service:'
            print '  name    =', name
            print '  regtype =', regtype
            print '  domain  =', domain
            logging.info('Service Registered!')
            logging.info(name)
            logging.info(regtype)
            logging.info(domain)


    sdRef = pybonjour.DNSServiceRegister(name = name,
                                         regtype = regtype,
                                         port = port,
                                         callBack = register_callback)

    try:
        try:
            while True:
                ready = select.select([sdRef], [], [])
                if sdRef in ready[0]:
                    pybonjour.DNSServiceProcessResult(sdRef)
        except Exception, e:
            logging.info(str(e))
    finally:
        sdRef.close()


if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', filename='/var/log/tdsurface/surfaceadaptoradvertise.log',level=logging.DEBUG,)
    
    register()
