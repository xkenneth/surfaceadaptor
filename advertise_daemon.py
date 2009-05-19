import sys
from daemon import Daemon
import logging
from advertise import register

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', filename='/var/log/tdsurface/surfaceadaptoradvertise.log',level=logging.DEBUG,)

class SurfaceAdaptorBonjourAdvertiseDaemon( Daemon ) :
    def run(self):
        
        logging.info("Advertising with Daemon.")

        register()
            
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
