import select
import sys
import pybonjour
from daemon import Daemon


class SurfaceAdaptorBonjourAdvertiseDaemon( Daemon ) :
    def run(self):
        name    = surface_adaptor
        regtype = _surface_adaptor._tcp
        port    = 8888


        def register_callback(sdRef, flags, errorCode, name, regtype, domain):
            if errorCode == pybonjour.kDNSServiceErr_NoError:
                print 'Registered service:'
                print '  name    =', name
                print '  regtype =', regtype
                print '  domain  =', domain


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
            except KeyboardInterrupt:
                pass
        finally:
            sdRef.close()

            
if __name__ == "__main__" :

	daemon = SurfaceAdaptorBonjourAdvertiseDaemon('/var/run/surfaceadaptoradvertisebonjour.pid')		

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
