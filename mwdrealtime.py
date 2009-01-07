import sys

slips = False
if len(sys.argv) != 4:
    print "Incorrect Arguments"
    sys.exit()

import status
import datetime

type = sys.argv[1]

time_stamp = sys.argv[2]

value = sys.argv[3]

#django setup code
from django.core.management import setup_environ

from tdsurface import settings

setup_environ(settings)

#setting up the slip model

from tdsurface.depth.models import MWDRealTime

#get the latest run

kwargs = {'run':status.current_run(),
          'time_stamp':time_stamp,
          'type':type,
          'value':float(value)}


print kwargs

t = MWDRealTime(**kwargs)

t.save()
