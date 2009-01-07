import sys

slips = False
if len(sys.argv) != 2:
    print "Incorrect Arguments"
    sys.exit()

if not(sys.argv[1] == 'in' or sys.argv[1] == 'out'):
    print "Invalid Arguments"
    sys.exit()

import status
import datetime

slips = 0
if sys.argv[1] == 'in':
    slips = 1

#django setup code
from django.core.management import setup_environ

from tdsurface import settings

setup_environ(settings)

#setting up the slip model

from tdsurface.depth.models import Slip
from tdsurface.depth.models import Run

#get the latest run


kwargs = {'run':status.current_run(),
          'time_stamp':str(datetime.datetime.now()),
          'status':slips}

print kwargs

t = Slip(**kwargs)

t.save()
